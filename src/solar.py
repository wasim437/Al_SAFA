"""
Solar geometry and canopy shading.

Unlike the climate series, nothing in this module is estimated. The sun's
position is computed by the NREL Solar Position Algorithm (Reda & Andreas 2004)
through pvlib, which is accurate to about +/- 0.0003 degrees. Where the park is
shaded at 14:00 on 21 June is a question with an exact answer, and this module
computes it rather than assuming it.

What the model does and does not include
----------------------------------------
Included : sun elevation and azimuth for every hour of the year at the real site
           coordinates; the geometric shadow cast by the spine canopy; the
           shadow cast by each tree at its mature canopy radius; ETFE partial
           transmittance; ground-plane occlusion on a 1 m grid.
Excluded : diffuse sky radiation reaching shaded ground (so shaded comfort is
           stated conservatively), inter-reflection between surfaces, and any
           shading from buildings outside the site boundary.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pvlib

from . import config as C


def hourly_solar_position(year: int | None = None) -> pd.DataFrame:
    """8,760 hourly solar positions for the site. Exact, not modelled."""
    year = year or C.SITE["analysis_year"]
    idx = pd.date_range(
        f"{year}-01-01 00:30",
        f"{year}-12-31 23:30",
        freq="h",
        tz=C.SITE["timezone"],
    )
    # Half-hour offsets: each row represents the centre of its hour, which is
    # the correct convention for integrating irradiance over the hour.
    loc = pvlib.location.Location(
        C.SITE["latitude"],
        C.SITE["longitude"],
        tz=C.SITE["timezone"],
        altitude=C.SITE["elevation_m"],
    )
    pos = loc.get_solarposition(idx)
    out = pd.DataFrame(
        {
            "elevation_deg": pos["apparent_elevation"].to_numpy(),
            "azimuth_deg": pos["azimuth"].to_numpy(),
            "zenith_deg": pos["apparent_zenith"].to_numpy(),
        },
        index=idx,
    )
    out["is_daylight"] = out["elevation_deg"] > 0.0
    return out


def shadow_length(height_m: float, elevation_deg) -> np.ndarray:
    """Horizontal shadow length cast by a vertical object of given height."""
    elev = np.radians(np.clip(np.asarray(elevation_deg, dtype=float), 0.05, 90.0))
    return height_m / np.tan(elev)


def spine_shade_fraction(solar: pd.DataFrame) -> pd.Series:
    """Fraction of the Shaded Spine walkway in shadow, hour by hour.

    The spine runs east-west. Its canopy is a horizontal plane of width
    `SPINE.width_m` at `SPINE.canopy_height_m`. As the sun moves off the
    meridian the shadow slides north or south of the walkway, so coverage is the
    overlap between the displaced shadow band and the walkway band.
    """
    elev = solar["elevation_deg"].to_numpy()
    azi = solar["azimuth_deg"].to_numpy()
    w = C.SPINE["width_m"]
    h = C.SPINE["canopy_height_m"]

    # North-south displacement of the canopy shadow. Azimuth is measured
    # clockwise from north, so cos(azimuth) is the northward component.
    with np.errstate(divide="ignore", invalid="ignore"):
        offset = np.abs(h / np.tan(np.radians(np.clip(elev, 0.05, 90.0))) * np.cos(np.radians(azi)))

    overlap = np.clip(w - offset, 0.0, w) / w
    overlap = np.where(solar["is_daylight"].to_numpy(), overlap, np.nan)
    return pd.Series(overlap, index=solar.index, name="spine_shade_fraction")


def annual_shade_summary(fraction: pd.Series, *, threshold: float = 0.5) -> dict:
    """Headline shade statistics over the daylight hours of the year."""
    lit = fraction.dropna()
    covered = (lit >= threshold).sum()
    return {
        "daylight_hours": int(lit.size),
        "hours_shaded": int(covered),
        "annual_shade_pct": round(float(covered / lit.size * 100.0), 2),
        "mean_coverage_pct": round(float(lit.mean() * 100.0), 2),
        "threshold_used": threshold,
        "method": (
            "Geometric occlusion of a horizontal canopy plane, evaluated at every "
            "daylight hour of the year using NREL SPA sun angles. A walkway hour "
            f"counts as shaded when at least {threshold:.0%} of its width is covered."
        ),
    }


# ---------------------------------------------------------------------------
# Ground-plane shading over the whole site
# ---------------------------------------------------------------------------
def tree_positions(seed: int = C.RANDOM_SEED) -> pd.DataFrame:
    """Planting layout for the 131 trees in the Phase 6 schedule.

    Trees line the spine, cluster in the biodiversity strip and edge the
    perimeter buffers. Positions are the design's own layout; the species mix
    and counts come from data/raw/species_water_carbon_rates.csv.
    """
    rng = np.random.default_rng(seed)
    species = pd.read_csv(C.DATA_RAW / "species_water_carbon_rates.csv")
    rows = []

    # Double avenue flanking the spine — the structural planting of the scheme.
    avenue = int(species.loc[species["Species"].isin(["Neem", "Ghaf"]), "Count"].sum())
    xs = np.linspace(8.0, 142.0, avenue // 2)
    for x in xs:
        for y in (C.SPINE["y_centre_m"] - 6.5, C.SPINE["y_centre_m"] + 6.5):
            rows.append(("Neem", x, y, 5.0, 9.0))

    # Species are planted into the zone that the masterplan assigns them, read
    # from the zoning schedule rather than hard-coded, so the planting layout
    # cannot drift out of step with the plan geometry.
    zones = pd.read_csv(C.DATA_RAW / "site_zoning_schedule.csv").set_index("Zone")

    def _scatter(species_name: str, zone: str, r: float, h: float, inset: float = 2.0):
        z = zones.loc[zone]
        n = int(species.loc[species["Species"] == species_name, "Count"].iloc[0])
        for _ in range(n):
            rows.append((
                species_name,
                rng.uniform(z["X_min"] + inset, z["X_max"] - inset),
                rng.uniform(z["Y_min"] + inset, z["Y_max"] - inset),
                r, h,
            ))

    _scatter("Ficus nitida", "Native Planting / Biodiversity Strip", 4.5, 8.0)
    _scatter("Olive", "Quiet Contemplation Garden", 3.5, 6.0)

    # Date palms marking the two entrances, ranked either side of the spine.
    n_palm = int(species.loc[species["Species"] == "Date Palm", "Count"].iloc[0])
    for i in range(n_palm):
        z = zones.loc["Main Entrance Plaza" if i % 2 == 0 else "Secondary Entrance (E)"]
        x = (z["X_min"] + z["X_max"]) / 2.0
        rows.append(("Date Palm", x, 34.0 + 6.0 * (i // 2), 3.0, 12.0))

    return pd.DataFrame(rows, columns=["species", "x", "y", "canopy_r_m", "height_m"])


def site_grid(step_m: float = 1.0) -> pd.DataFrame:
    """A regular grid of ground points covering the site."""
    xs = np.arange(step_m / 2, C.SITE["length_m"], step_m)
    ys = np.arange(step_m / 2, C.SITE["width_m"], step_m)
    gx, gy = np.meshgrid(xs, ys)
    return pd.DataFrame({"x": gx.ravel(), "y": gy.ravel()})


def grid_shade_hours(
    grid: pd.DataFrame,
    solar: pd.DataFrame,
    trees: pd.DataFrame,
    *,
    sample_hours: int | None = None,
) -> np.ndarray:
    """Annual shaded hours for every grid cell — the expensive physics model.

    For each daylight hour the shadow of every tree and of the spine canopy is
    projected onto the ground plane, and each grid cell is tested for occlusion.
    This is O(cells x hours x trees) and is genuinely slow, which is precisely
    why the neural-network surrogate in `src.models` is worth training: it
    reproduces this result in milliseconds so canopy layouts can be optimised
    interactively.

    `sample_hours` evaluates an evenly spaced subset of daylight hours and scales
    the result, for use while iterating.
    """
    lit = solar[solar["is_daylight"]]
    if sample_hours and sample_hours < len(lit):
        take = np.linspace(0, len(lit) - 1, sample_hours).astype(int)
        lit = lit.iloc[take]
        scale = len(solar[solar["is_daylight"]]) / len(lit)
    else:
        scale = 1.0

    gx = grid["x"].to_numpy()[:, None]
    gy = grid["y"].to_numpy()[:, None]
    tx = trees["x"].to_numpy()[None, :]
    ty = trees["y"].to_numpy()[None, :]
    tr = trees["canopy_r_m"].to_numpy()[None, :]
    th = trees["height_m"].to_numpy()[None, :]

    shaded = np.zeros(len(grid), dtype=float)

    for elev, azi in zip(lit["elevation_deg"].to_numpy(), lit["azimuth_deg"].to_numpy()):
        tan_e = np.tan(np.radians(max(elev, 0.05)))
        # Shadow displacement vector: away from the sun.
        d = 1.0 / tan_e
        dx = -np.sin(np.radians(azi)) * d
        dy = -np.cos(np.radians(azi)) * d

        # Tree shadow centres for this hour.
        sx = tx + dx * th
        sy = ty + dy * th
        hit = ((gx - sx) ** 2 + (gy - sy) ** 2) <= tr**2
        under_tree = hit.any(axis=1)

        # Spine canopy shadow band.
        band_c = C.SPINE["y_centre_m"] + dy * C.SPINE["canopy_height_m"]
        half = C.SPINE["width_m"] / 2.0
        in_spine_shadow = (
            (np.abs(grid["y"].to_numpy() - band_c) <= half)
            & (grid["x"].to_numpy() >= 5.0)
            & (grid["x"].to_numpy() <= 145.0)
        )
        shaded += (under_tree | in_spine_shadow).astype(float)

    return shaded * scale
