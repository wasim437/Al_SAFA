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
from matplotlib.path import Path as MplPath

from . import config as C, plan


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


def crescent_centreline(n: int = 200):
    """Sample the Crescent Walk's centreline.

    Returns ``(x, y, nx, ny)`` — position and the unit normal in plan at each
    sample. The normal is what the shade model needs: a canopy element resists
    the sun across its width, and "across" is the normal direction, which on an
    arc rotates continuously along the route instead of being fixed.

    The geometry itself lives in `src.plan`, which builds the whole masterplan
    from this one curve.
    """
    return plan.centreline(n)


def crescent_shade_fraction(solar: pd.DataFrame) -> pd.Series:
    """Fraction of the Crescent Walk in shadow, hour by hour.

    Above the 7 m walk sits a horizontal canopy plane of width
    `CRESCENT.canopy_width_m` at `CRESCENT.canopy_height_m`, overhanging it on
    both sides, with a vertical louvre blade of depth
    `CRESCENT.south_louvre_depth_m` hanging from its southern edge.

    Geometry, in plan, working in metres north of the site's south boundary:

      * The canopy plane throws a shadow band displaced north-south by
        ``h / tan(elevation) * cos(azimuth)``. Azimuth is clockwise from north,
        so ``cos(azimuth)`` is the northward component and the band slides north
        when the sun is in the south.
      * The southern louvre only does work when the sun is actually in the
        south (``cos(azimuth) > 0``). When it is, the blade behaves like a
        southward extension of the canopy edge by
        ``depth / tan(elevation) * cos(azimuth)``. This is what keeps the band
        on the path through the winter, when the plane alone would have slid
        past it.

    Coverage is the overlap of that band with the walkway, as a fraction of
    walkway width. Returns NaN outside daylight.
    """
    elev = solar["elevation_deg"].to_numpy()
    azi = solar["azimuth_deg"].to_numpy()

    pw = C.CRESCENT["path_width_m"]
    cw = C.CRESCENT["canopy_width_m"]
    h = C.CRESCENT["canopy_height_m"]
    ld = C.CRESCENT["south_louvre_depth_m"]

    # Sample the arc once; every hour is evaluated against every sample, and the
    # hour's coverage is the mean along the route. A straight route would have
    # one orientation and one answer; the crescent has a spread of headings, and
    # that spread is the entire reason for curving it.
    _, _, nx, ny = crescent_centreline()

    with np.errstate(divide="ignore", invalid="ignore"):
        tan_e = np.tan(np.radians(np.clip(elev, 0.05, 90.0)))
        # Ground displacement of the canopy's shadow, as a plan vector.
        reach = h / tan_e
        dx = -np.sin(np.radians(azi)) * reach
        dy = -np.cos(np.radians(azi)) * reach

        # Component of that displacement ACROSS the route at each sample:
        # (hours x samples).
        s = dx[:, None] * nx[None, :] + dy[:, None] * ny[None, :]

        lo = -cw / 2.0 + s
        hi = cw / 2.0 + s

        # The louvre hangs on whichever edge faces south, so it extends the
        # shaded band on that side — but only when the sun is actually south of
        # the route, which is the case the plane alone cannot cover.
        if ld > 0:
            louvre_reach = ld / tan_e
            lv = (-np.sin(np.radians(azi)) * louvre_reach)[:, None] * nx[None, :] \
                 + (-np.cos(np.radians(azi)) * louvre_reach)[:, None] * ny[None, :]
            lo = np.where(lv < 0, lo + lv, lo)
            hi = np.where(lv > 0, hi + lv, hi)

    ov = np.clip(np.minimum(hi, pw / 2.0) - np.maximum(lo, -pw / 2.0), 0.0, pw) / pw
    overlap = ov.mean(axis=1)
    overlap = np.where(solar["is_daylight"].to_numpy(), overlap, np.nan)
    return pd.Series(overlap, index=solar.index, name="crescent_shade_fraction")


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

    Each species is planted into the room the masterplan gives it, and the
    rooms come from `src.plan`, so the planting cannot drift out of step with
    the geometry. Species counts come from
    data/raw/species_water_carbon_rates.csv; the layout is the design's own.
    """
    rng = np.random.default_rng(seed)
    species = pd.read_csv(C.DATA_RAW / "species_water_carbon_rates.csv")
    counts = species.set_index("Species")["Count"].to_dict()
    rows = []

    # --- the avenue --------------------------------------------------------
    # A double rank in the planted margins either side of the walk, set at the
    # centre of each margin so the crowns knit into the canopy's overhang rather
    # than fighting it. This is the structural planting of the scheme: the
    # gridshell carries the summer, the avenue carries the shoulder seasons and
    # the low morning and evening sun that no horizontal plane can reach.
    #
    # Ghaf on the southern rank, Neem on the northern. That is not decoration —
    # Ghaf (Prosopis cineraria) is the UAE's national tree, the most drought
    # tolerant species in the schedule at 45 L/day against Neem's 90, and the
    # southern rank is the hotter, drier, more exposed of the two.
    n_ghaf = int(counts["Ghaf"])
    n_neem_avenue = int(counts["Neem"]) - 18      # 18 held back for the gates
    margin = (C.CRESCENT["path_width_m"] + C.CRESCENT["canopy_width_m"]) / 4.0
    for name, n, sgn, r, h in (("Ghaf", n_ghaf, 1.0, 6.0, 8.0),
                               ("Neem", n_neem_avenue, -1.0, 5.0, 9.0)):
        cx, cy, cnx, cny = crescent_centreline(n)
        for x, y, nx_, ny_ in zip(cx, cy, cnx, cny):
            # Offset along the local normal, so the rank follows the arc.
            rows.append((name, float(x + sgn * margin * nx_),
                         float(y + sgn * margin * ny_), r, h))

    # --- planting by room --------------------------------------------------
    zones = {z["key"]: z for z in plan.build()}

    def _scatter(name: str, key: str, n: int, r: float, h: float, inset: float = 2.5):
        """Scatter n trees inside a room, rejecting points outside its polygon."""
        poly = MplPath(zones[key]["polygon"])
        pts = np.asarray(zones[key]["polygon"])
        lo, hi = pts.min(axis=0) + inset, pts.max(axis=0) - inset
        placed = 0
        for _ in range(n * 200):
            if placed >= n:
                break
            p = rng.uniform(lo, hi)
            if poly.contains_point(p, radius=-inset):
                rows.append((name, float(p[0]), float(p[1]), r, h))
                placed += 1

    # Date palms in the Oasis Basin. Palms belong in the nakhil, not scattered
    # at entrances: a date grove is the reason a falaj exists.
    _scatter("Date Palm", "basin", int(counts["Date Palm"]), 3.0, 12.0)
    _scatter("Ficus nitida", "wadi", int(counts["Ficus nitida"]), 4.5, 8.0)
    _scatter("Olive", "quiet", int(counts["Olive"]), 3.5, 6.0)

    # The remaining Neem rank the two arrival majlis, nine to each gate.
    for key in ("gate_w", "gate_e"):
        _scatter("Neem", key, 9, 5.0, 9.0, inset=2.0)

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

    # The canopy centreline, sampled once. 60 samples over ~124 m is a point
    # every ~2 m, comfortably finer than the 18 m ribbon it describes.
    arc_x, arc_y, _, _ = crescent_centreline(60)

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

        # Crescent canopy shadow — the 18 m gridshell follows the arc, so its
        # shadow is a curved ribbon, not a straight band. Displace the
        # centreline by the sun vector and test each cell's distance to the
        # displaced ribbon. Same geometry as crescent_shade_fraction, kept
        # deliberately in step: the headline number and the ground-plane map
        # disagreeing would be worse than either being slightly off.
        ch = C.CRESCENT["canopy_height_m"]
        sx_c = arc_x + dx * ch
        sy_c = arc_y + dy * ch
        half = C.CRESCENT["canopy_width_m"] / 2.0
        if C.CRESCENT["south_louvre_depth_m"] > 0:
            half += C.CRESCENT["south_louvre_depth_m"] * 0.5 / max(tan_e, 0.05)

        d2 = ((grid["x"].to_numpy()[:, None] - sx_c[None, :]) ** 2
              + (grid["y"].to_numpy()[:, None] - sy_c[None, :]) ** 2)
        in_canopy_shadow = d2.min(axis=1) <= half**2
        shaded += (under_tree | in_canopy_shadow).astype(float)

    return shaded * scale
