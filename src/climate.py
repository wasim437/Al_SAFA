"""
Climate physics: thermal comfort indices and the monthly-to-hourly downscaling.

HONESTY NOTE — read this before quoting any hourly figure
---------------------------------------------------------
The National Center of Meteorology publishes Dubai climate as **monthly
normals**. This project needs an **hourly** series to train and test a machine
learning model on 8,760 rows. The gap between the two is bridged by the
`downscale_to_hourly` function below, which is a *model*, not a measurement.

Everything it produces is therefore labelled MODELLED wherever it appears, in
the notebook, in the figures and in the reports. The monthly means of the
modelled series reproduce the published normals exactly by construction — that
is the constraint the model is fitted under, and it is asserted as a test in
`tests/test_climate.py`. What the model cannot reproduce is real day-to-day
weather variance: a heat wave, a shamal, a cloudy fortnight. Conclusions in this
project are therefore drawn about the *typical* year, never about extremes.

Buying an AMY (actual meteorological year) or TMY hourly file from NCM would
remove this step entirely and is the first recommendation for any funded
continuation of this work.

References
----------
Rothfusz, L.P. (1990). The Heat Index Equation. NWS Southern Region
    Technical Attachment SR/SSD 90-23.
Parton, W.J. & Logan, J.A. (1981). A model for diurnal variation in soil and
    air temperature. Agricultural Meteorology 23, 205-216.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from . import config as C


# ---------------------------------------------------------------------------
# Thermal comfort
# ---------------------------------------------------------------------------
def heat_index_c(temp_c, rh_pct):
    """NWS Heat Index ("feels like" temperature) in degrees Celsius.

    Vectorised over numpy arrays or pandas Series. Below 26.7 C (80 F) the
    Rothfusz regression is not valid and the NWS simple form is used instead,
    exactly as the published method specifies.
    """
    t_c = np.asarray(temp_c, dtype=float)
    rh = np.asarray(rh_pct, dtype=float)
    t_f = t_c * 9.0 / 5.0 + 32.0

    # Simple form, used below 80 F and averaged with the full form at the seam.
    simple = 0.5 * (t_f + 61.0 + (t_f - 68.0) * 1.2 + rh * 0.094)

    full = (
        -42.379
        + 2.04901523 * t_f
        + 10.14333127 * rh
        - 0.22475541 * t_f * rh
        - 0.00683783 * t_f**2
        - 0.05481717 * rh**2
        + 0.00122874 * t_f**2 * rh
        + 0.00085282 * t_f * rh**2
        - 0.00000199 * t_f**2 * rh**2
    )

    # The two published adjustments the shortened versions of this formula omit.
    dry_adj = ((13.0 - rh) / 4.0) * np.sqrt(
        np.clip(17.0 - np.abs(t_f - 95.0), 0.0, None) / 17.0
    )
    full = np.where((rh < 13.0) & (t_f > 80.0) & (t_f < 112.0), full - dry_adj, full)

    wet_adj = ((rh - 85.0) / 10.0) * ((87.0 - t_f) / 5.0)
    full = np.where((rh > 85.0) & (t_f > 80.0) & (t_f < 87.0), full + wet_adj, full)

    hi_f = np.where(t_f < 80.0, simple, full)
    return (hi_f - 32.0) * 5.0 / 9.0


def comfort_band(heat_index_celsius):
    """Classify a heat index into one of the four project comfort bands."""
    hi = np.asarray(heat_index_celsius, dtype=float)
    out = np.empty(hi.shape, dtype=object)
    for name, lo, hi_lim in C.COMFORT_BANDS:
        out[(hi >= lo) & (hi < hi_lim)] = name
    return out


def apply_shade(temp_c, rh_pct, *, relief_c: float = C.SHADE_TEMP_RELIEF_C):
    """Air temperature and humidity under canopy shade.

    Shade lowers air temperature by `relief_c`. Because absolute moisture is
    unchanged while the air cools, relative humidity rises — ignoring that would
    overstate the comfort benefit, since humidity is what makes Gulf heat
    dangerous. The rise is computed through the Magnus saturation-pressure
    relation rather than assumed.
    """
    t = np.asarray(temp_c, dtype=float)
    rh = np.asarray(rh_pct, dtype=float)

    def _svp(tc):  # saturation vapour pressure, hPa (Magnus, Alduchov-Eskridge)
        return 6.1094 * np.exp(17.625 * tc / (tc + 243.04))

    t_shaded = t - relief_c
    vapour = rh / 100.0 * _svp(t)
    rh_shaded = np.clip(vapour / _svp(t_shaded) * 100.0, 0.0, 100.0)
    return t_shaded, rh_shaded


# ---------------------------------------------------------------------------
# Monthly -> hourly downscaling  (MODELLED — see the note at the top)
# ---------------------------------------------------------------------------
def downscale_to_hourly(normals: pd.DataFrame, solar: pd.DataFrame) -> pd.DataFrame:
    """Reconstruct an 8,760-hour series from 12 rows of monthly normals.

    The diurnal shape follows Parton & Logan (1981): a sine rise from sunrise to
    a peak lagged after solar noon, then an exponential decay overnight. The
    shape is anchored to the *real* sunrise and sunset times for this latitude,
    which come from the pvlib solar model rather than from an assumption.

    Parameters
    ----------
    normals : the 12-row NCM table
    solar   : the 8,760-row solar position table from `src.solar`, which supplies
              the true daylight window for every day of the year.

    Returns a frame indexed by the same hourly timestamps as `solar`.
    """
    if len(normals) != 12:
        raise ValueError(f"expected 12 monthly normals, got {len(normals)}")

    idx = solar.index
    hour = idx.hour + idx.minute / 60.0

    # Smooth the monthly normals around the year so December flows into January
    # instead of stepping. Without this the series has 12 discontinuities that a
    # tree model will happily learn as if they were real.
    def _smooth_monthly(col: str) -> np.ndarray:
        v = normals[col].to_numpy(dtype=float)
        # day-of-year of each month's midpoint, wrapped
        mid = np.array([15, 45, 74, 105, 135, 166, 196, 227, 258, 288, 319, 349], float)
        doy = idx.dayofyear.to_numpy(dtype=float)
        ext_mid = np.concatenate([mid - 365.0, mid, mid + 365.0])
        ext_val = np.concatenate([v, v, v])
        return np.interp(doy, ext_mid, ext_val)

    t_max = _smooth_monthly("TempMax_C")
    t_min = _smooth_monthly("TempMin_C")
    rh_mean = _smooth_monthly("RH_pct")
    wind = _smooth_monthly("WindSpeed_kmh")
    ghi_day = _smooth_monthly("SolarGHI_kWh_m2_day")

    # Real daylight window per day, from the solar model.
    daylight = solar["elevation_deg"] > 0
    per_day = pd.DataFrame({"day": idx.dayofyear, "light": daylight, "h": hour})
    lit = per_day[per_day["light"]]
    sunrise = lit.groupby("day")["h"].min().reindex(range(1, 367)).ffill().bfill()
    sunset = lit.groupby("day")["h"].max().reindex(range(1, 367)).ffill().bfill()
    sr = sunrise.reindex(idx.dayofyear).to_numpy()
    ss = sunset.reindex(idx.dayofyear).to_numpy()

    daylen = np.clip(ss - sr, 1e-6, None)
    lag = 2.0        # peak temperature lags solar noon by ~2 h
    night_k = 2.2    # nocturnal cooling rate constant

    # Daytime: sine from sunrise (t_min) to the lagged afternoon peak (t_max).
    phase = np.pi * (hour - sr) / (daylen + 2.0 * lag)
    day_t = t_min + (t_max - t_min) * np.sin(np.clip(phase, 0.0, np.pi))

    # Night: exponential decay from the temperature at sunset toward t_min.
    t_sunset = t_min + (t_max - t_min) * np.sin(
        np.clip(np.pi * (ss - sr) / (daylen + 2.0 * lag), 0.0, np.pi)
    )
    hours_since_set = np.where(hour > ss, hour - ss, hour + 24.0 - ss)
    night_len = np.clip(24.0 - daylen, 1e-6, None)
    night_t = t_min + (t_sunset - t_min) * np.exp(-night_k * hours_since_set / night_len)

    is_day = (hour >= sr) & (hour <= ss)
    temp = np.where(is_day, day_t, night_t)

    # Relative humidity moves inversely to temperature across the day. Absolute
    # moisture is held near constant within a day, which is the physically
    # correct behaviour and is what makes Dubai nights feel worse than the air
    # temperature alone suggests.
    t_daily_mean = 0.5 * (t_max + t_min)
    rh = np.clip(rh_mean * (1.0 + 0.030 * (t_daily_mean - temp)), 5.0, 100.0)

    # Distribute the daily GHI total over the daylight hours by sine shape.
    sin_elev = np.clip(np.sin(np.radians(solar["elevation_deg"].to_numpy())), 0.0, None)
    day_sum = pd.Series(sin_elev, index=idx).groupby(idx.dayofyear).transform("sum")
    ghi = np.where(day_sum > 0, ghi_day * 1000.0 * sin_elev / day_sum, 0.0)

    out = pd.DataFrame(
        {
            "temp_c": temp,
            "rh_pct": rh,
            "wind_kmh": wind,
            "ghi_wh_m2": ghi,
        },
        index=idx,
    )
    out["heat_index_c"] = heat_index_c(out["temp_c"], out["rh_pct"])
    return out


def verify_downscaling(hourly: pd.DataFrame, normals: pd.DataFrame) -> pd.DataFrame:
    """Check the modelled hourly series against the published normals.

    This is the test that keeps the downscaling honest. If the modelled series
    drifts from the published normals, the model is wrong and the error belongs
    in the report, not hidden.

    A subtlety worth stating, because getting it wrong silently corrupts every
    comfort figure: NCM's ``TempMax_C`` is the **mean daily maximum** for the
    month, not the hottest reading in it. The correct comparison is therefore
    the mean of the modelled *daily* maxima against that normal. Comparing the
    single hottest modelled hour against it compares two different quantities
    and will always show a spurious error.
    """
    daily = hourly.groupby(hourly.index.dayofyear).agg(
        day_max=("temp_c", "max"),
        day_min=("temp_c", "min"),
        day_mean=("temp_c", "mean"),
        month=("temp_c", lambda s: s.index[0].month),
    )
    m = daily.groupby("month")
    got = pd.DataFrame({
        "modelled_mean_max": m["day_max"].mean(),
        "modelled_mean_min": m["day_min"].mean(),
        "modelled_mean": m["day_mean"].mean(),
    })
    got.index.name = "MonthNum"
    ref = normals.set_index("MonthNum")[["TempMax_C", "TempMin_C", "TempAvg_C"]]
    cmp = got.join(ref)
    cmp["err_max_c"] = cmp["modelled_mean_max"] - cmp["TempMax_C"]
    cmp["err_min_c"] = cmp["modelled_mean_min"] - cmp["TempMin_C"]
    cmp["err_mean_c"] = cmp["modelled_mean"] - cmp["TempAvg_C"]
    return cmp
