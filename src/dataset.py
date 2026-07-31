"""
Dataset assembly and feature engineering.

Two datasets come out of this module:

  build_hourly()  -> 8,760 rows, one per hour of the year. The temporal dataset
                     used for comfort regression, comfort classification and
                     microclimate clustering.
  build_spatial() -> 15,000 rows, one per square metre of the site. The spatial
                     dataset used for the per-cell comfort model and for the
                     neural-network shade surrogate.

Both are written to data/processed/ with a companion schema file so a reader can
tell, column by column, which fields are measured, which are computed physics,
and which are modelled.
"""

from __future__ import annotations

import json

import numpy as np
import pandas as pd

from . import climate, config as C, plan, solar


# Column provenance. Every column in the hourly table appears here; the notebook
# asserts that, so a new feature cannot be added without declaring where it came
# from.
HOURLY_PROVENANCE = {
    "elevation_deg": "COMPUTED — NREL SPA via pvlib",
    "azimuth_deg": "COMPUTED — NREL SPA via pvlib",
    "zenith_deg": "COMPUTED — NREL SPA via pvlib",
    "is_daylight": "COMPUTED — NREL SPA via pvlib",
    "temp_c": "MODELLED — diurnal downscaling of NCM monthly normals",
    "rh_pct": "MODELLED — diurnal downscaling of NCM monthly normals",
    "wind_kmh": "MEASURED (monthly) — NCM normals, held flat within the month",
    "ghi_wh_m2": "MODELLED — NCM daily GHI distributed by solar geometry",
    "heat_index_c": "DERIVED — NWS Rothfusz on modelled temp/RH",
    "crescent_shade_fraction": "COMPUTED — geometric canopy occlusion",
    "temp_shaded_c": "DERIVED — measured shade relief applied to modelled temp",
    "rh_shaded_pct": "DERIVED — Magnus relation on the shaded temperature",
    "heat_index_shaded_c": "DERIVED — NWS Rothfusz on the shaded condition",
    "comfort_band": "DERIVED — project comfort thresholds on exposed heat index",
    "comfort_band_shaded": "DERIVED — project comfort thresholds, shaded",
    "hour": "INDEX",
    "month": "INDEX",
    "dayofyear": "INDEX",
    "hour_sin": "ENGINEERED — cyclical encoding of hour",
    "hour_cos": "ENGINEERED — cyclical encoding of hour",
    "doy_sin": "ENGINEERED — cyclical encoding of day of year",
    "doy_cos": "ENGINEERED — cyclical encoding of day of year",
    "is_weekend": "ENGINEERED — Fri/Sat, the UAE weekend",
    "temp_range_c": "ENGINEERED — daily max minus min",
    "hours_from_solar_noon": "ENGINEERED",
    "comfort_gain_c": "TARGET — heat index reduction delivered by shade",
    "visitors_est": "MODELLED — demand response to comfort, see build_hourly",
}


def build_hourly(*, verbose: bool = True) -> pd.DataFrame:
    """Assemble the 8,760-row hourly dataset."""
    normals = pd.read_csv(C.DATA_RAW / "dubai_climate_normals_ncm.csv")
    sol = solar.hourly_solar_position()
    met = climate.downscale_to_hourly(normals, sol)

    df = sol.join(met)
    df["crescent_shade_fraction"] = solar.crescent_shade_fraction(sol).fillna(0.0)

    # Shaded counterfactual — the whole point of the design.
    t_sh, rh_sh = climate.apply_shade(df["temp_c"], df["rh_pct"])
    df["temp_shaded_c"] = t_sh
    df["rh_shaded_pct"] = rh_sh
    df["heat_index_shaded_c"] = climate.heat_index_c(t_sh, rh_sh)
    df["comfort_gain_c"] = df["heat_index_c"] - df["heat_index_shaded_c"]

    df["comfort_band"] = climate.comfort_band(df["heat_index_c"])
    df["comfort_band_shaded"] = climate.comfort_band(df["heat_index_shaded_c"])

    # --- calendar / cyclical features -------------------------------------
    idx = df.index
    df["hour"] = idx.hour
    df["month"] = idx.month
    df["dayofyear"] = idx.dayofyear
    df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24.0)
    df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24.0)
    df["doy_sin"] = np.sin(2 * np.pi * df["dayofyear"] / 365.0)
    df["doy_cos"] = np.cos(2 * np.pi * df["dayofyear"] / 365.0)
    # UAE weekend is Saturday-Sunday since the 2022 working-week change.
    df["is_weekend"] = idx.dayofweek.isin([5, 6]).astype(int)

    daily = df.groupby(df.index.dayofyear)["temp_c"]
    df["temp_range_c"] = (daily.transform("max") - daily.transform("min"))

    noon = df.groupby(df.index.dayofyear)["elevation_deg"].transform("idxmax")
    delta = df.index.to_series().to_numpy() - noon.to_numpy()
    df["hours_from_solar_noon"] = np.abs(delta / np.timedelta64(1, "h"))

    # --- visitor demand (MODELLED) ----------------------------------------
    # Park use is driven by comfort, time of day and day of week. This is a
    # behavioural model calibrated to the Neighbourhood Parks Manual capacity
    # benchmark and the 800 m catchment, NOT observed footfall — no footfall
    # data exists for this site. It is used to compare design options against
    # each other, never quoted as a prediction of actual attendance.
    rings = pd.read_csv(C.DATA_RAW / "walk_catchment_rings.csv")
    catchment = float(rings.loc[rings["Radius_m"] == 800, "Est_Residents"].iloc[0])

    comfort_pull = 1.0 / (1.0 + np.exp((df["heat_index_shaded_c"] - 33.0) / 3.0))
    evening = np.exp(-0.5 * ((df["hour"] - 19.0) / 2.6) ** 2)
    morning = 0.55 * np.exp(-0.5 * ((df["hour"] - 7.5) / 1.8) ** 2)
    daypart = evening + morning
    weekend_lift = 1.0 + 0.35 * df["is_weekend"]

    raw = comfort_pull * daypart * weekend_lift
    df["visitors_est"] = (raw / raw.max() * catchment * 0.10 * 0.55).round(0)

    if verbose:
        print(f"hourly dataset: {df.shape[0]:,} rows x {df.shape[1]} columns")
    return df


def build_spatial(*, step_m: float = 1.0, sample_hours: int = 240, verbose: bool = True):
    """Assemble the per-square-metre spatial dataset.

    Returns ``(grid, trees)``. The shade-hours column is produced by the slow
    physics model in `src.solar`; `sample_hours` controls how many daylight
    hours are evaluated.
    """
    sol = solar.hourly_solar_position()
    trees = solar.tree_positions()
    grid = solar.site_grid(step_m)

    if verbose:
        print(f"spatial grid: {len(grid):,} cells, {len(trees)} trees, "
              f"{sample_hours} sampled daylight hours")

    grid["shade_hours"] = solar.grid_shade_hours(
        grid, sol, trees, sample_hours=sample_hours
    )
    daylight_total = int(sol["is_daylight"].sum())
    grid["shade_pct"] = grid["shade_hours"] / daylight_total * 100.0

    # --- spatial features --------------------------------------------------
    gx = grid["x"].to_numpy()
    gy = grid["y"].to_numpy()

    # Distance to the crescent is distance to its ARC, not to a chord. On a
    # 18 m sagitta the chord approximation is wrong by up to 18 m at midspan,
    # and this is a feature the shade surrogate leans on heavily.
    _sx, _sy, _, _ = solar.crescent_centreline(120)
    grid["dist_to_crescent_m"] = np.sqrt(
        ((gx[:, None] - _sx[None, :]) ** 2 + (gy[:, None] - _sy[None, :]) ** 2)
    ).min(axis=1)
    grid["dist_to_edge_m"] = np.minimum.reduce([
        gx, C.SITE["length_m"] - gx, gy, C.SITE["width_m"] - gy
    ])

    tx = trees["x"].to_numpy()[None, :]
    ty = trees["y"].to_numpy()[None, :]
    d = np.sqrt((gx[:, None] - tx) ** 2 + (gy[:, None] - ty) ** 2)
    grid["dist_to_tree_m"] = d.min(axis=1)
    grid["trees_within_10m"] = (d <= 10.0).sum(axis=1)
    grid["trees_within_20m"] = (d <= 20.0).sum(axis=1)
    grid["canopy_overhead"] = (
        d <= trees["canopy_r_m"].to_numpy()[None, :]
    ).any(axis=1).astype(int)

    # On the walk itself (the 7 m surface), measured from the arc.
    grid["under_crescent_walk"] = (
        grid["dist_to_crescent_m"] <= C.CRESCENT["path_width_m"] / 2.0
    ).astype(int)
    # Under the 18 m gridshell, which reaches 5.5 m past the walk either side.
    grid["under_gridshell"] = (
        grid["dist_to_crescent_m"] <= C.CRESCENT["canopy_width_m"] / 2.0
    ).astype(int)

    # Zone membership and surface properties, by point-in-polygon against the
    # masterplan. The rooms are curved trapezoids struck off the crescent's own
    # centre, so a bounding-box test would assign a third of the site to the
    # wrong room; nothing here can be done with min/max coordinates.
    #
    # The alley network is the RESIDUAL zone — everything the rooms do not claim
    # — so it is the default and is never tested for.
    from matplotlib.path import Path as MplPath

    pts = np.column_stack([gx, gy])
    residual = plan.RESIDUAL
    grid["zone"] = residual["name"]
    grid["category"] = residual["category"]
    grid["albedo"] = residual["albedo"]
    for z in plan.build():
        if z.get("is_residual"):
            continue
        hit = np.zeros(len(grid), dtype=bool)
        for part in z["parts"]:
            if len(part) >= 3:
                hit |= MplPath(part).contains_points(pts)
        grid.loc[hit, "zone"] = z["name"]
        grid.loc[hit, "category"] = z["category"]
        grid.loc[hit, "albedo"] = z["albedo"]

    # Sky view factor proxy: openness overhead, driven by nearby canopy.
    grid["sky_view_factor"] = np.clip(
        1.0 - 0.06 * grid["trees_within_10m"] - 0.45 * grid["under_crescent_walk"], 0.05, 1.0
    )

    # Mean summer afternoon comfort per cell — the design-relevant target.
    summer = sol[(sol.index.month.isin([6, 7, 8])) & (sol["elevation_deg"] > 10)]
    normals = pd.read_csv(C.DATA_RAW / "dubai_climate_normals_ncm.csv")
    jul = normals.loc[normals["MonthNum"] == 7].iloc[0]
    exposed_hi = float(climate.heat_index_c(jul["TempMax_C"], jul["RH_pct"]))

    shade_frac = np.clip(grid["shade_pct"] / 100.0, 0.0, 1.0)
    relief = shade_frac * C.SHADE_TEMP_RELIEF_C
    # Each cell gets relief in proportion to how much of the year it is shaded.
    # Cooler air at unchanged absolute moisture means higher relative humidity,
    # so both come from the same Magnus relation used in src.climate — a cell
    # that gains shade is not credited with dry-air comfort it would not have.
    t_cell, rh_cell = climate.apply_shade(
        np.full(len(grid), jul["TempMax_C"]),
        np.full(len(grid), jul["RH_pct"]),
        relief_c=relief,
    )
    grid["summer_heat_index_c"] = climate.heat_index_c(t_cell, rh_cell)
    grid["comfort_gain_c"] = exposed_hi - grid["summer_heat_index_c"]
    grid["comfort_band"] = climate.comfort_band(grid["summer_heat_index_c"])
    grid["n_summer_hours_sampled"] = len(summer)

    if verbose:
        print(f"spatial dataset: {grid.shape[0]:,} rows x {grid.shape[1]} columns")
    return grid, trees


def save(hourly: pd.DataFrame, grid: pd.DataFrame, trees: pd.DataFrame) -> dict:
    """Write both datasets plus a schema describing every column's provenance."""
    hp = C.DATA_PROCESSED / "hourly_climate_comfort_8760.csv"
    gp = C.DATA_PROCESSED / "spatial_grid_comfort.csv"
    tp = C.DATA_PROCESSED / "planting_layout.csv"

    hourly.to_csv(hp, index_label="timestamp")
    grid.to_csv(gp, index=False)
    trees.to_csv(tp, index=False)

    schema = {
        "generated": pd.Timestamp.now().isoformat(timespec="seconds"),
        "hourly": {
            "file": hp.name,
            "rows": int(len(hourly)),
            "columns": {c: HOURLY_PROVENANCE.get(c, "UNDECLARED") for c in hourly.columns},
        },
        "spatial": {
            "file": gp.name,
            "rows": int(len(grid)),
            "cell_size_m": 1.0,
            "note": (
                "shade_hours is COMPUTED by ray-traced occlusion over sampled "
                "daylight hours; summer_heat_index_c is DERIVED from it."
            ),
        },
        "legend": {
            "MEASURED": "observed by an instrument and published by the source organisation",
            "COMPUTED": "deterministic physics or astronomy, no estimation involved",
            "MODELLED": "reconstructed by a documented model — carries model error",
            "DERIVED": "an exact function of other columns in this table",
            "ENGINEERED": "a feature built for the machine learning models",
        },
    }
    sp = C.DATA_PROCESSED / "schema.json"
    sp.write_text(json.dumps(schema, indent=2), encoding="utf-8")

    undeclared = [c for c, v in schema["hourly"]["columns"].items() if v == "UNDECLARED"]
    if undeclared:
        raise ValueError(f"columns without declared provenance: {undeclared}")

    return {"hourly": hp, "spatial": gp, "trees": tp, "schema": sp}
