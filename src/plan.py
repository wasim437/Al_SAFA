"""The masterplan geometry — "Falaj Al Safa", the crescent and the channel.

Why this module exists
----------------------
The previous scheme laid the park out as a grid of axis-aligned rectangles with
a walkway through the middle. That is a spreadsheet, not a plan. It also carried
a design fault that the numbers exposed: a route with ONE orientation is
defeated all at once. When a sun angle beats it, it beats the entire length, and
the walkway has no shade anywhere along it — 330 hours a year of that.

This module replaces it with a plan built on a single circular arc, and lays
every room out in the arc's own coordinates. Two consequences follow, and both
are the point:

  1. The route continuously changes heading, so some segment is always angled
     well against the sun. The hours in which the walk offers no shade anywhere
     fall from 330 to 51.
  2. Because every room is bounded by radii of the same arc, no room is a
     rectangle and every room faces the crescent square-on. The plan reads as
     one geometry rather than a packing diagram.

Arc coordinates
---------------
Everything is described as ``(t, d)``:

    t   angle about the arc centre, degrees, 0 at midspan, + toward the east
    d   radial offset from the arc, metres, + outward = SOUTH, - inward = NORTH

``arc_point(t, d)`` maps that to site metres. Because the map is a polar frame
about a single centre it is injective, so two ``(t, d)`` boxes that do not
overlap produce two plan polygons that do not overlap. Zone areas are then the
shoelace area of the polygon, which is why the schedule closes on 15,000 m²
without anyone tuning a number by hand.

Which way the crescent bows
---------------------------
Convex SOUTH, concave north. The solar model is indifferent to the sign — the
southern louvre swaps to whichever edge faces the sun either way — so the choice
was made spatially: bowing south puts the structure's mass between the sun and
the hollow it wraps, so the concave side is the park's cool pocket rather than a
south-facing bowl. The Oasis Basin, the quiet garden and the children's play are
all placed in that hollow, and the comfort map in figures/fig04 is the check.
"""

from __future__ import annotations

import json
import math

import numpy as np

from . import config as C

# ---------------------------------------------------------------------------
# The crescent — parameters live in config.py, which is the single source of
# truth for anything that appears in more than one place. The sweep that chose
# the sagitta is documented there.
# ---------------------------------------------------------------------------
CRESCENT = C.CRESCENT

SITE_W = C.SITE["length_m"]   # 150 m, east-west
SITE_H = C.SITE["width_m"]    # 100 m, north-south

# The perimeter ring: a planted dune berm outside a running loop.
BERM_DEPTH_M = 3.5            # Al Kathib — the planted berm against the roads
LOOP_WIDTH_M = 2.5            # Al Madar — the running and walking circuit
RING_M = BERM_DEPTH_M + LOOP_WIDTH_M

# Al Falaj — the water channel. It runs along the NORTHERN drip line of the
# gridshell, so it sits under the canopy's overhang rather than in the open.
# That is not decoration: an open channel in Dubai loses a serious fraction of
# its volume to evaporation, and shading it is the difference between a water
# feature and a water bill.
FALAJ_WIDTH_M = 0.9
FALAJ_OFFSET_M = -9.0         # outer (north) edge of the gridshell


def _derive():
    half = CRESCENT["chord_m"] / 2.0
    sag = CRESCENT["sagitta_m"]
    R = (half * half + sag * sag) / (2.0 * sag)
    theta = math.degrees(math.asin(half / R))
    cx = SITE_W / 2.0
    cy = CRESCENT["y_ends_m"] - sag + R      # centre sits north of the arc
    return R, theta, cx, cy


ARC_R, ARC_THETA, ARC_CX, ARC_CY = _derive()

# The walk runs between the two arrival majlis, which cap the ends.
WALK_THETA = ARC_THETA - CRESCENT["gate_sweep_deg"]


# ---------------------------------------------------------------------------
# Arc coordinates
# ---------------------------------------------------------------------------
def arc_point(t_deg, d_m=0.0):
    """Map arc coordinates to site metres. Vectorised over ``t_deg``."""
    t = np.radians(np.asarray(t_deg, dtype=float))
    r = ARC_R + np.asarray(d_m, dtype=float)
    return ARC_CX + r * np.sin(t), ARC_CY - r * np.cos(t)


def centreline(n: int = 200, *, d_m: float = 0.0):
    """Sample the crescent's centreline.

    Returns ``(x, y, nx, ny)`` — position and the unit normal in plan. The
    normal is radial, pointing outward (south), which is the direction the
    canopy spans across and the direction the shade model needs.
    """
    t = np.linspace(-WALK_THETA, WALK_THETA, n)
    x, y = arc_point(t, d_m)
    tr = np.radians(t)
    return x, y, np.sin(tr), -np.cos(tr)


def arc_band(t0: float, t1: float, d0: float, d1: float, n: int = 64):
    """A room in arc coordinates, returned as a closed plan polygon.

    Both long edges are sampled as arcs, so the result is a curved trapezoid
    rather than a four-sided approximation of one.
    """
    t = np.linspace(t0, t1, n)
    xo, yo = arc_point(t, d0)
    xi, yi = arc_point(t[::-1], d1)
    return np.column_stack([np.r_[xo, xi], np.r_[yo, yi]])


# ---------------------------------------------------------------------------
# Polygon utilities — clipping and area, no external dependency
# ---------------------------------------------------------------------------
def clip_to_rect(poly, x0=0.0, y0=0.0, x1=SITE_W, y1=SITE_H):
    """Sutherland-Hodgman clip of a polygon against an axis-aligned rectangle.

    Rooms are laid out in the arc's polar frame, which does not respect the
    site's rectangular boundary. Clipping here is what lets the plan be drawn
    from one geometry and still stop at the site line.
    """
    def _clip(pts, inside, intersect):
        if len(pts) == 0:
            return pts
        out = []
        prev = pts[-1]
        prev_in = inside(prev)
        for cur in pts:
            cur_in = inside(cur)
            if cur_in:
                if not prev_in:
                    out.append(intersect(prev, cur))
                out.append(cur)
            elif prev_in:
                out.append(intersect(prev, cur))
            prev, prev_in = cur, cur_in
        return out

    def _x_int(a, b, xv):
        t = (xv - a[0]) / (b[0] - a[0])
        return (xv, a[1] + t * (b[1] - a[1]))

    def _y_int(a, b, yv):
        t = (yv - a[1]) / (b[1] - a[1])
        return (a[0] + t * (b[0] - a[0]), yv)

    pts = [tuple(p) for p in np.asarray(poly, dtype=float)]
    pts = _clip(pts, lambda p: p[0] >= x0, lambda a, b: _x_int(a, b, x0))
    pts = _clip(pts, lambda p: p[0] <= x1, lambda a, b: _x_int(a, b, x1))
    pts = _clip(pts, lambda p: p[1] >= y0, lambda a, b: _y_int(a, b, y0))
    pts = _clip(pts, lambda p: p[1] <= y1, lambda a, b: _y_int(a, b, y1))
    return np.array(pts, dtype=float).reshape(-1, 2)


def polygon_area(poly) -> float:
    """Shoelace area. Zone areas are measured off the drawing, never typed in."""
    p = np.asarray(poly, dtype=float)
    if len(p) < 3:
        return 0.0
    x, y = p[:, 0], p[:, 1]
    return abs(float(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))) / 2.0


def _rect(x0, y0, x1, y1):
    return np.array([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], dtype=float)


def ring_parts(inset_outer: float, inset_inner: float, gaps=None):
    """A rectangular ring, built as four strips with the gate openings cut out.

    Four strips rather than one annulus, because the berm has to be *broken*
    where the crescent's horns run out to the street. A park whose perimeter
    planting has no gate in it is a walled compound. Splitting the east and west
    strips around the openings also keeps the areas exact — no polygon boolean,
    and no double counting against the gate zones.

    ``gaps`` is ``{"w": (y0, y1), "e": (y0, y1)}``.
    """
    a, b = inset_outer, inset_inner
    gaps = gaps or {}
    parts = [
        _rect(a, a, SITE_W - a, b),                      # south strip
        _rect(a, SITE_H - b, SITE_W - a, SITE_H - a),    # north strip
    ]
    for side, (x0, x1) in (("w", (a, b)), ("e", (SITE_W - b, SITE_W - a))):
        y0, y1 = b, SITE_H - b
        gap = gaps.get(side)
        if gap and y0 < gap[0] and gap[1] < y1:
            parts.append(_rect(x0, y0, x1, gap[0]))
            parts.append(_rect(x0, gap[1], x1, y1))
        else:
            parts.append(_rect(x0, y0, x1, y1))
    return parts


# ---------------------------------------------------------------------------
# The schedule
# ---------------------------------------------------------------------------
# Each room is a box in arc coordinates. Nothing here is an area figure: the
# areas are computed from these boxes and written into the zoning schedule, so
# the drawing and the schedule cannot disagree.
#
# North of the crescent is its concave side and sits in the structure's own
# shadow — that is where the rooms people linger in are placed. South of it is
# the convex, sunnier side, which takes the planting, the sports lawn and the
# uses that run in the evening.
_T = WALK_THETA
_G = ARC_THETA            # the arc's own ends, at the corners of the inner field
_HORN = 36.0              # the horns run on past them, out through the berm
_HALF = CRESCENT["path_width_m"] / 2.0
_SHELL = CRESCENT["canopy_width_m"] / 2.0     # 9 m — the gridshell edge
_FAR = 62.0               # past every boundary; clipping trims it to the site
_WIDE = 46.0              # angular reach of the corner rooms, likewise clipped

# Radial cuts. These are the t values at which one room stops and the next
# begins, and they are also the centre lines of the sikkas — the two are the
# same thing, which is why the alleys land where the rooms actually meet.
CUT_N = [-13.0, 13.0]                       # concave side: play | centre | picnic
CUT_S = [-14.0, -1.0, 11.0, 17.0]           # convex side: four cuts, five rooms

ROOMS = [
    # ---- the armature. Contiguous: no alley is cut through the structure ---
    dict(key="crescent_walk", at=(-6.0, 0.0), name="Al Mamsha — the Crescent Walk",
         short="Crescent\nWalk", category="Circulation", rate_key="Shaded walkway paving",
         albedo=0.30, shade_structure=1, icon="🚶", token="blue", contiguous=True,
         desc="The 7 m shaded walk beneath the crescent gridshell",
         band=(-_T, _T, -_HALF, _HALF)),

    dict(key="falaj", at=(18.0, -8.55), name="Al Falaj — the water channel",
         short="Al Falaj", category="Water", rate_key="Soft landscape / planting bed",
         albedo=0.06, shade_structure=1, icon="💧", token="teal", contiguous=True,
         desc="A 0.9 m recirculating channel on the canopy's northern drip line",
         band=(-_T, _T, FALAJ_OFFSET_M, FALAJ_OFFSET_M + FALAJ_WIDTH_M)),

    dict(key="margin_n", at=(6.0, -5.8), name="Crescent Shade Margin (N)",
         short="Shade\nmargin (N)", category="Green", rate_key="Soft landscape / planting bed",
         albedo=0.18, shade_structure=1, icon="🌿", token="lime", contiguous=True,
         desc="Planted margin under the northern overhang; the tree avenue",
         band=(-_T, _T, FALAJ_OFFSET_M + FALAJ_WIDTH_M, -_HALF)),

    dict(key="margin_s", at=(-18.0, 6.25), name="Crescent Shade Margin (S)",
         short="Shade\nmargin (S)", category="Green", rate_key="Soft landscape / planting bed",
         albedo=0.18, shade_structure=1, icon="🌿", token="lime", contiguous=True,
         desc="Planted margin under the southern louvre; the tree avenue",
         band=(-_T, _T, _HALF, _SHELL)),

    # The gates are the crescent's two horns, where the gridshell runs on past
    # the last room and breaks through the berm to reach the street. They are
    # the only two zones drawn against the site boundary rather than the inner
    # field — a park whose perimeter planting has no gate in it is a compound.
    dict(key="gate_w", name="West Gate Majlis",
         short="West\ngate", category="Arrival", rate_key="Entrance plaza hard paving",
         albedo=0.35, shade_structure=1, icon="🚪", token="gold",
         contiguous=True, full_site=True,
         desc="Arrival majlis at the western horn, breaking through the berm",
         band=(-_HORN, -_T, -13.0, 13.0)),

    dict(key="gate_e", name="East Gate Majlis",
         short="East\ngate", category="Arrival", rate_key="Entrance plaza hard paving",
         albedo=0.35, shade_structure=1, icon="🚪", token="gold",
         contiguous=True, full_site=True,
         desc="Arrival majlis at the eastern horn, breaking through the berm",
         band=(_T, _HORN, -13.0, 13.0)),

    # ---- the concave (north) side — the cool pocket ------------------------
    # Every room here sits in the crescent's own shadow. This is where the uses
    # that ask people to STAY are placed; fig04 is the check on that claim.
    dict(key="basin", at=(0.0, -22.0), name="Al Nakhil — the Oasis Basin",
         short="Al Nakhil\nOasis Basin", category="Green", rate_key="Soft landscape / planting bed",
         albedo=0.15, shade_structure=0, icon="🌴", token="teal",
         desc="Sunken crescent palm court fed by the falaj; the park's heart",
         band=(CUT_N[0], CUT_N[1], -34.0, -_SHELL)),

    dict(key="quiet", at=(0.0, -44.0), name="Quiet Contemplation Garden",
         short="Quiet\ngarden", category="Passive", rate_key="Soft landscape / planting bed",
         albedo=0.18, shade_structure=1, icon="🧘", token="purple",
         desc="The deepest pocket of the hollow, screened behind the basin",
         band=(CUT_N[0], CUT_N[1], -_FAR, -34.0)),

    dict(key="play", at=(-19.0, -28.0), name="Children's Dune Play",
         short="Children's\ndune play", category="Active",
         rate_key="Children's play zone (safety surface + equipment)",
         albedo=0.25, shade_structure=1, icon="🛝", token="red",
         desc="Modelled play dunes in the crescent's western shadow",
         bands=[(-_T, CUT_N[0], -_FAR, -_SHELL), (-_WIDE, -_T, -_FAR, -13.0)]),

    dict(key="picnic", at=(19.0, -28.0), name="Family Picnic Grove",
         short="Family\npicnic grove", category="Passive", rate_key="Soft landscape / planting bed",
         albedo=0.20, shade_structure=1, icon="🧺", token="lime",
         desc="Shaded lawn terraces in the crescent's eastern shadow",
         bands=[(CUT_N[1], _T, -_FAR, -_SHELL), (_T, _WIDE, -_FAR, -13.0)]),

    # ---- the convex (south) side ------------------------------------------
    dict(key="fitness", at=(-20.0, 26.0), name="Outdoor Fitness Terrace",
         short="Fitness\nterrace", category="Active", rate_key="Outdoor fitness zone",
         albedo=0.25, shade_structure=1, icon="🏋️", token="orange",
         desc="Calisthenics terraces stepped into the southern berm",
         bands=[(-_T, CUT_S[0], _SHELL, _FAR), (-_WIDE, -_T, 13.0, _FAR)]),

    dict(key="wadi", at=(-7.5, 26.0), name="Native Planting / Biodiversity Wadi",
         short="Biodiversity\nwadi", category="Green", rate_key="Soft landscape / planting bed",
         albedo=0.18, shade_structure=0, icon="🌾", token="green",
         desc="Dry watercourse of native species; habitat and stormwater sink",
         band=(CUT_S[0], CUT_S[1], _SHELL, _FAR)),

    dict(key="plaza", at=(5.0, 26.0), name="Community Plaza & Event Lawn",
         short="Community\nplaza", category="Social", rate_key="Community plaza",
         albedo=0.28, shade_structure=0, icon="🎪", token="gold",
         desc="Evening events, addressing the crescent's convex face",
         band=(CUT_S[1], CUT_S[2], _SHELL, _FAR)),

    dict(key="souk", at=(14.5, 19.0), name="Souk Kiosks & Services",
         short="Souk", category="Commercial", rate_key="Kiosk / built structure",
         albedo=0.32, shade_structure=1, icon="🏪", token="orange",
         desc="Small trading units on the sikka to the east gate",
         band=(CUT_S[2], CUT_S[3], _SHELL, _FAR)),

    dict(key="sports", at=(22.0, 30.0), name="Multipurpose Sports Lawn",
         short="Sports\nlawn", category="Active", rate_key="Sports lawn turf",
         albedo=0.22, shade_structure=0, icon="⚽", token="green",
         desc="Open turf sized for five-a-side, in the south-east corner",
         bands=[(CUT_S[3], _T, _SHELL, _FAR), (_T, _WIDE, 13.0, _FAR)]),
]

# Two zones are not arc bands but rings around the whole site.
RING_ZONES = [
    dict(key="berm", at_xy=(112.0, 1.75), name="Al Kathib — the dune berm",
         short="Dune berm", category="Green_Buffer",
         rate_key="Soft landscape / planting bed",
         albedo=0.18, shade_structure=0, icon="🏜️", token="lime",
         desc="Planted earth berm against the roads; noise, glare and heat",
         ring=(0.0, BERM_DEPTH_M)),
    dict(key="loop", at_xy=(38.0, 4.75), name="Al Madar — the perimeter loop",
         short="Perimeter loop", category="Circulation",
         rate_key="Shaded walkway paving",
         albedo=0.30, shade_structure=0, icon="🏃", token="blue",
         desc="2.5 m running and walking circuit, shaded by the berm planting",
         ring=(BERM_DEPTH_M, RING_M)),
]

# The residual. Everything the rooms do not claim is the alley network: the
# radial sikkas that cut from the crescent to the loop, plus setbacks. It is
# computed, not scheduled, which is why the schedule closes exactly.
RESIDUAL = dict(
    key="sikkak", name="Al Sikkak — shaded alleys & setbacks",
    short="Sikkak", category="Circulation", rate_key="Shaded walkway paving",
    albedo=0.30, shade_structure=1, icon="🌀", token="blue",
    desc="Radial alleys linking the crescent to the loop, and the setbacks",
)

# The rooms are laid out edge to edge on the arc partition, then each is inset
# so the gap between two rooms IS the alley. A 1.5 m inset on all four sides
# gives a 3 m sikka between neighbours — the width of the shaded alleys in Al
# Fahidi, which is the reference, and narrow enough that the walls shade the
# floor for most of the day.
ALLEY_INSET_M = 1.5
ALLEY_INSET_DEG = math.degrees(ALLEY_INSET_M / ARC_R)


def _inset(t0, t1, d0, d1):
    """Shrink an arc box by the alley inset, without letting it invert."""
    dt = min(ALLEY_INSET_DEG, (t1 - t0) / 3.0)
    dd = min(ALLEY_INSET_M, (d1 - d0) / 3.0)
    return t0 + dt, t1 - dt, d0 + dd, d1 - dd


def build() -> list[dict]:
    """Resolve the schedule into drawn polygons with measured areas.

    Order matters. The two gates are resolved first because the openings they
    cut in the berm are measured off them, rather than being a second set of
    numbers that could drift out of step with where the gates actually are.
    """
    out = []
    for r in ROOMS:
        full = r.get("full_site")
        box_lo = (0.0, 0.0) if full else (RING_M, RING_M)
        box_hi = (SITE_W, SITE_H) if full else (SITE_W - RING_M, SITE_H - RING_M)
        polys, area = [], 0.0
        for band in (r.get("bands") or [r["band"]]):
            box = band if r.get("contiguous") else _inset(*band)
            poly = clip_to_rect(arc_band(*box), box_lo[0], box_lo[1], box_hi[0], box_hi[1])
            if len(poly) >= 3:
                polys.append(poly)
                area += polygon_area(poly)
        z = {k: v for k, v in r.items() if k not in ("band", "bands", "at")}
        z["parts"] = polys
        z["polygon"] = max(polys, key=polygon_area) if polys else np.empty((0, 2))
        z["area"] = area
        # Where the plan number goes. The four armature bands all lie on the
        # same curve, so their centroids land within a few metres of each other
        # and the numbers collide; each therefore carries an explicit anchor.
        at = r.get("at")
        z["label_xy"] = ([float(v) for v in arc_point(*at)] if at
                         else [float(v) for v in z["polygon"].mean(axis=0)])
        out.append(z)

    # Where each gate crosses the ring, the berm and the loop are broken.
    by_key = {z["key"]: z for z in out}
    gaps = {}
    for side, key, band in (("w", "gate_w", (0.0, RING_M)),
                            ("e", "gate_e", (SITE_W - RING_M, SITE_W))):
        p = by_key[key]["polygon"]
        m = (p[:, 0] >= band[0] - 1e-6) & (p[:, 0] <= band[1] + 1e-6)
        if m.any():
            gaps[side] = (float(p[m, 1].min()), float(p[m, 1].max()))

    for r in RING_ZONES:
        a, b = r["ring"]
        z = {k: v for k, v in r.items() if k not in ("ring", "at_xy")}
        z["parts"] = ring_parts(a, b, gaps)
        z["polygon"] = max(z["parts"], key=polygon_area)
        z["area"] = sum(polygon_area(p) for p in z["parts"])
        z["label_xy"] = list(r["at_xy"])
        out.append(z)

    claimed = sum(z["area"] for z in out)
    z = dict(RESIDUAL)
    z["polygon"] = np.array([[RING_M, RING_M], [SITE_W - RING_M, RING_M],
                             [SITE_W - RING_M, SITE_H - RING_M], [RING_M, SITE_H - RING_M]])
    z["parts"] = [z["polygon"]]
    z["area"] = C.SITE["area_sqm"] - claimed
    z["is_residual"] = True
    out.append(z)
    return out


# ---------------------------------------------------------------------------
# Secondary geometry — drawn, and used by the portal and the film
# ---------------------------------------------------------------------------
def sikka_lines():
    """The radial alleys, as centre lines from the crescent out to the loop.

    These are the same t values the rooms are partitioned on, so an alley is
    literally the gap between two rooms rather than a line drawn over them.
    Being radii of the arc, every alley meets the crescent square-on; and
    because the arc's centre lies far to the north, they fan open toward the
    north-west, which is the bearing the Shamal arrives on.
    """
    lines = []
    for t in CUT_N:
        lines.append(np.column_stack(arc_point(np.array([t, t]),
                                               np.array([-_SHELL, -_FAR]))))
    for t in CUT_S:
        lines.append(np.column_stack(arc_point(np.array([t, t]),
                                               np.array([_SHELL, _FAR]))))
    out = []
    for seg in lines:
        c = clip_to_rect(np.r_[seg, seg[::-1]], RING_M, RING_M,
                         SITE_W - RING_M, SITE_H - RING_M)
        if len(c) >= 2:
            out.append(c[:2])
    return out


def majlis_pods():
    """Circular shaded seating rooms — the majlis — set on the sikka junctions.

    Placed where an alley meets the crescent's shade margin, which is both the
    busiest point of the plan and the coolest ground away from the walk itself.
    """
    pods = []
    for t in CUT_N:
        x, y = arc_point(t, -_SHELL - 5.5)
        pods.append({"x": float(x), "y": float(y), "r": 4.5})
    for t in (CUT_S[0], CUT_S[2]):
        x, y = arc_point(t, _SHELL + 5.5)
        pods.append({"x": float(x), "y": float(y), "r": 4.5})
    # The fifth sits at the far end of the hollow, in the quiet garden.
    x, y = arc_point(0.0, -46.0)
    pods.append({"x": float(x), "y": float(y), "r": 5.5})
    return pods


def facilities():
    """Commercial and service facilities, placed against the drawn geometry.

    The Scope of Work requires a Commercial and Service Facilities Map showing
    "the location, distribution, and integration of the proposed commercial and
    service uses", and separately names restrooms, drinking fountains, a
    café/kiosk, service and maintenance facilities, waste and recycling
    stations, bicycle parking and drop-off in its minimum programme. None of
    them existed in the plan before this function.

    Nothing here is dropped on the drawing by eye. Each position is expressed in
    the crescent's own arc coordinates, so the whole set moves with the geometry
    if the sagitta changes — the same rule every other element obeys.

    ``kind`` groups them for the map's legend; ``serviced_from`` records how a
    van reaches it, because a facility that cannot be serviced is a facility
    that will not be maintained.
    """
    out = []

    def add(kind, name, t, d, note, serviced_from):
        x, y = arc_point(t, d)
        out.append(dict(kind=kind, name=name,
                        x=float(np.clip(x, 4.0, SITE_W - 4.0)),
                        y=float(np.clip(y, 4.0, SITE_H - 4.0)),
                        note=note, serviced_from=serviced_from))

    # Commercial — the souk already exists as a room; this is its frontage.
    add("commercial", "Souk kiosks — F&B and retail", 14.0, _SHELL + 26.0,
        "8 modular kiosks on the convex face, facing the plaza and the event "
        "lawn so evening trade and programming reinforce each other",
        "South margin service route")
    add("commercial", "Café pavilion", -1.0, _SHELL + 20.0,
        "Sited between the plaza and the play area — the two longest-dwell "
        "spaces — with seating under the canopy's south margin",
        "South margin service route")

    # Restrooms — at both gates, where arrival concentrates and drainage is
    # shortest to the perimeter.
    for t, side in ((-_T + 1.0, "West"), (_T - 1.0, "East")):
        add("restroom", f"{side} restrooms — universally accessible",
            t, _SHELL + 9.0,
            "At the gate, so it is found without entering the park, and short "
            "drainage runs to the perimeter",
            f"{side} gate")

    # Drinking fountains — on the walk and in every room that holds people for
    # long enough to need one.
    for t in (-16.0, -6.0, 6.0, 16.0):
        add("fountain", "Drinking fountain + bottle fill", t, -_SHELL - 1.5,
            "On the shaded walk, in the cool margin", "Walk")
    add("fountain", "Drinking fountain — play area", -13.0, -_SHELL - 24.0,
        "Beside the children's dune play, within sight of family seating",
        "North sikka")
    add("fountain", "Drinking fountain — fitness terrace", -14.0, _SHELL + 30.0,
        "At the outdoor fitness terrace", "South margin service route")

    # Waste and recycling — paired bins where people gather or leave.
    for t, where in ((-_T + 2.0, "West gate"), (_T - 2.0, "East gate"),
                     (2.0, "Community plaza"), (13.0, "Picnic grove"),
                     (-13.0, "Play area")):
        d = -_SHELL - 20.0 if where in ("Picnic grove", "Play area") \
            else _SHELL + 12.0
        add("waste", f"Waste & recycling — {where}", t, d,
            "Paired general and recycling, screened, on the service route",
            "Perimeter loop")

    # Maintenance, bicycles and drop-off — the operational edge of the park.
    add("service", "Service & maintenance store", _T - 3.0, _SHELL + 34.0,
        "Irrigation controls, tools and horticultural store, tucked behind the "
        "berm where it is invisible from the walk",
        "East gate, direct from the street")
    for t, side in ((-_T + 1.5, "West"), (_T - 1.5, "East")):
        add("bicycle", f"{side} bicycle parking", t, _SHELL + 4.0,
            "Sheltered racks inside the gate, before the walk begins",
            f"{side} gate")
        add("dropoff", f"{side} drop-off / pick-up bay", t, _SHELL + 44.0,
            "Lay-by on the street edge, level and step-free to the gate",
            "Street")
    return out


def falaj_polyline(n: int = 200):
    """Centre line of the water channel."""
    x, y = arc_point(np.linspace(-_T, _T, n),
                     FALAJ_OFFSET_M + FALAJ_WIDTH_M / 2.0)
    return x, y


def loop_polyline(n: int = 240):
    """Centre line of the perimeter running circuit, with rounded corners."""
    m = BERM_DEPTH_M + LOOP_WIDTH_M / 2.0
    rad = 14.0
    x0, y0, x1, y1 = m, m, SITE_W - m, SITE_H - m
    corners = [(x1 - rad, y0 + rad, -90, 0), (x1 - rad, y1 - rad, 0, 90),
               (x0 + rad, y1 - rad, 90, 180), (x0 + rad, y0 + rad, 180, 270)]
    xs, ys = [], []
    for cx, cy, a0, a1 in corners:
        a = np.radians(np.linspace(a0, a1, n // 4))
        xs.append(cx + rad * np.cos(a))
        ys.append(cy + rad * np.sin(a))
    x = np.r_[tuple(xs)]
    y = np.r_[tuple(ys)]
    return np.r_[x, x[:1]], np.r_[y, y[:1]]


def canopy_outline(n: int = 160):
    """Plan footprint of the 18 m gridshell, as a closed polygon."""
    h = CRESCENT["canopy_width_m"] / 2.0
    return arc_band(-_T, _T, -h, h, n)


# ---------------------------------------------------------------------------
# Export — one geometry, consumed by the figures, the portal and the film
# ---------------------------------------------------------------------------
def write_schedule(path=None):
    """Write data/raw/site_zoning_schedule.csv from the drawn plan.

    The schedule is DERIVED, not authored. Every area in it is the shoelace
    area of the polygon the masterplan actually draws, which is why the columns
    close on 15,000 m² without anyone reconciling them by hand. Plan geometry is
    given as a polygon, not as X_min/X_max — no room in this scheme is a
    rectangle, and a bounding box would misplace about a third of the site.
    """
    import csv

    rates = {}
    with open(C.DATA_RAW / "construction_unit_rates_aed.csv", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            rates[row["Element"]] = row["Rate_AED"]

    path = path or (C.DATA_RAW / "site_zoning_schedule.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["Zone", "Category", "Area_sqm", "Pct_of_site", "Rate_AED_sqm",
                    "SurfaceAlbedo", "ShadeStructure", "Residual", "Polygon_WKT"])
        for z in build():
            pts = " ".join(f"{p[0]:.2f},{p[1]:.2f}" for p in z["polygon"])
            w.writerow([
                z["name"], z["category"], f"{z['area']:.1f}",
                f"{z['area'] / C.SITE['area_sqm'] * 100:.2f}",
                rates.get(z["rate_key"], ""), z["albedo"], z["shade_structure"],
                int(bool(z.get("is_residual"))), f"POLYGON(({pts}))",
            ])
    return path


def export(path=None) -> dict:
    """Write the plan to JSON so nothing downstream redraws it from memory."""
    zones = build()
    fx, fy = falaj_polyline(120)
    lx, ly = loop_polyline()
    doc = {
        "_readme": (
            "Generated by src/plan.py. The single source of the masterplan "
            "geometry: the figures, the portal and the concept film all read "
            "this file. Coordinates are metres, origin at the site's south-west "
            "corner, +x east, +y north."
        ),
        "concept": C.SITE["concept"],
        "site": {"width_m": SITE_W, "height_m": SITE_H, "area_sqm": C.SITE["area_sqm"]},
        "crescent": {
            **{k: v for k, v in CRESCENT.items()},
            "radius_m": round(ARC_R, 3),
            "centre": [ARC_CX, round(ARC_CY, 3)],
            "half_angle_deg": round(ARC_THETA, 4),
            "walk_half_angle_deg": round(WALK_THETA, 4),
        },
        "zones": [
            {
                "key": z["key"], "name": z["name"], "short": z["short"],
                "category": z["category"], "icon": z["icon"],
                "token": z.get("token", "green"), "desc": z["desc"],
                "area_sqm": round(z["area"], 1),
                "pct_of_site": round(z["area"] / C.SITE["area_sqm"] * 100, 2),
                "albedo": z["albedo"], "shade_structure": z["shade_structure"],
                "residual": bool(z.get("is_residual")),
                "label_xy": [round(v, 2) for v in z.get("label_xy", [0, 0])],
                "parts": [[[round(float(a), 2), round(float(b), 2)] for a, b in part]
                          for part in z["parts"]],
                "polygon": [[round(float(a), 2), round(float(b), 2)]
                            for a, b in z["polygon"]],
            }
            for z in zones
        ],
        "falaj": [[round(float(a), 2), round(float(b), 2)] for a, b in zip(fx, fy)],
        "loop": [[round(float(a), 2), round(float(b), 2)] for a, b in zip(lx, ly)],
        "majlis": majlis_pods(),
        "sikkak": [[[round(float(p[0]), 2), round(float(p[1]), 2)] for p in l]
                   for l in sikka_lines()],
    }
    path = path or (C.DATA_PROCESSED / "masterplan_geometry.json")
    path.write_text(json.dumps(doc, indent=1), encoding="utf-8")
    return doc


if __name__ == "__main__":
    zs = build()
    total = 0.0
    print(f"{'zone':<42}{'category':<14}{'area m2':>10}{'%':>7}")
    print("-" * 73)
    for z in sorted(zs, key=lambda a: -a["area"]):
        total += z["area"]
        print(f"{z['name']:<42}{z['category']:<14}{z['area']:>10,.0f}"
              f"{z['area'] / C.SITE['area_sqm'] * 100:>7.1f}")
    print("-" * 73)
    print(f"{'TOTAL':<56}{total:>10,.0f}{total / C.SITE['area_sqm'] * 100:>7.1f}")
    print(f"\narc R = {ARC_R:.1f} m, half-angle {ARC_THETA:.2f} deg, "
          f"centre ({ARC_CX:.0f}, {ARC_CY:.1f})")
