"""
Al Safa 2 Park — AI Design Challenge
Single source of truth for site constants, model settings and the visual system.

Every number that appears in more than one place lives here. If a figure in the
report disagrees with a figure in the notebook, it is a bug in the code that
consumes this file — not a difference of opinion between two scripts.

Project : Dubai Municipality AI Park Design Challenge — Al Safa 2 Park
Concept : "Falaj Al Safa" — the crescent and the channel
Author  : Mohamed Wasim
"""

from __future__ import annotations

from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent

DATA_RAW = ROOT / "data" / "raw"
DATA_INTERIM = ROOT / "data" / "interim"
DATA_PROCESSED = ROOT / "data" / "processed"
FIGURES = ROOT / "figures"
MODELS = ROOT / "models"
NOTEBOOKS = ROOT / "notebooks"

for _p in (DATA_RAW, DATA_INTERIM, DATA_PROCESSED, FIGURES, MODELS):
    _p.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Site — Al Safa 2 Park, Dubai
# ---------------------------------------------------------------------------
SITE = {
    "name": "Al Safa 2 Park",
    "concept": "Falaj Al Safa",
    "concept_subtitle": "a crescent of shade over a channel of water",
    "city": "Dubai, United Arab Emirates",
    # Coordinates used for every solar computation (NREL SPA via pvlib).
    "latitude": 25.190,
    "longitude": 55.238,
    "elevation_m": 5.0,
    "timezone": "Asia/Dubai",  # UTC+4, no daylight saving
    # Site envelope. NOTE: the 150 x 100 m rectangle is an assumption pending
    # confirmation against the supplied DWG. Every area figure depends on it.
    "area_sqm": 15000.0,
    "length_m": 150.0,
    "width_m": 100.0,
    "boundary_status": "ASSUMED 150x100 m rectangle - verify against Al Safa Park 2 Plan (5).dwg",
    # Analysis year for the 8,760-hour solar model.
    "analysis_year": 2026,
    "budget_aed": 35_000_000,
}

# AL HILAL — the Crescent Canopy. The single arc the whole park is built on.
#
# THE SECTION
# -----------
# An earlier version put a 9 m canopy directly over a 9 m walkway at 5.5 m,
# which shades well at summer noon and then fails completely from November to
# January: Dubai's winter sun sits at 41° in the SOUTH, so the shadow slides
# clean off the path. Measured annual coverage was 61%, and December was 0%.
#
# The section was solved rather than styled. Three moves fix it:
#   1. Narrow the walk and widen the canopy, so the plane overhangs 5.5 m either
#      side and the shadow has somewhere to fall.
#   2. Drop the canopy to 4.5 m — lower plane, shorter throw, better low sun.
#   3. Hang a 3 m louvre blade on the SOUTH edge. This is the piece that buys
#      the winter, and it is ordinary hot-climate architecture: a deep southern
#      brise-soleil, the same logic as a mashrabiya screen.
#
# THE PLAN
# --------
# The route is a single circular arc — a crescent — not a bar and not a wave.
#
# A straight route presents ONE orientation, so when a sun angle defeats it, it
# defeats the whole length at once and the walk has no shade anywhere along it.
# That is 330 hours a year. An arc changes heading continuously, so some segment
# is always angled well.
#
# The depth of the bow was swept against the 8,760-hour solar model, not chosen.
# Every row below was measured at the section fixed above, over all 4,402
# daylight hours of the year:
#
#     plan form                 mean cover   worst month   hours with NO shade
#     straight east-west bar       87.4%        68.7%              330
#     sine meander (superseded)    85.0%        73.1%               63
#     arc, sagitta 10 m            87.1%        70.2%              116
#     arc, sagitta 14 m            86.6%        71.3%               62
#     arc, sagitta 18 m            85.9%        72.1%               52   <- adopted
#     arc, sagitta 22 m            84.9%        72.3%               61
#     closed elliptical loop       79.1%        69.8%               89
#
# 18 m is the minimum of the last column. Deeper bows and closed loops both
# lose, for the same reason: they force more of the route to run north-south,
# and a canopy over a north-south route can only work when the sun is low in the
# east or west.
#
# Be careful reading the first column. The straight bar has the HIGHEST mean
# coverage of anything tested — an east-west canopy is near the optimum
# orientation for 25°N, and curving it costs a point. The crescent is not
# claimed to shade more ground on average. It is claimed to remove the hours in
# which the route offers nowhere at all to stand, and it removes six sevenths of
# them. That is the trade, stated in the direction that is not flattering.
#
# The route actually built runs between the two gate majlis, so it is slightly
# shorter than the full arc and its heading spread slightly narrower:
# 86.4% mean, 71.6% worst month, 56 hours with no shade.
#
# The arc bows convex-SOUTH. The solar model is indifferent to that sign — the
# louvre swaps to whichever edge faces the sun — so the choice was spatial:
# bowing south puts the structure between the sun and the hollow it wraps, so
# the concave side becomes the park's cool pocket instead of a south-facing
# bowl. Every room people are asked to linger in sits in that hollow.
#
# The full plan — rooms, alleys, basin, berm — is generated from this arc in
# src/plan.py. Nothing there is a hand-typed coordinate.
# The sweep above, as data rather than only as a comment, so the reports and the
# boards can cite it instead of restating it by hand. (name, mean cover %, worst
# month %, hours with no shade anywhere, adopted?)
PLAN_FORM_SWEEP = [
    ("Straight east–west bar",      87.4, 68.7, 330, False),
    ("Sine meander (superseded)",   85.0, 73.1,  63, False),
    ("Arc, sagitta 10 m",           87.1, 70.2, 116, False),
    ("Arc, sagitta 14 m",           86.6, 71.3,  62, False),
    ("Arc, sagitta 18 m",           85.9, 72.1,  52, True),
    ("Arc, sagitta 22 m",           84.9, 72.3,  61, False),
    ("Closed elliptical loop",      79.1, 69.8,  89, False),
]

CRESCENT = {
    "chord_m": 138.0,             # east-west span, horn to horn
    "sagitta_m": 18.0,            # depth of the bow at midspan
    "y_ends_m": 59.0,             # northing of the two ends
    "path_width_m": 7.0,          # Al Mamsha — the walkable surface
    "canopy_width_m": 18.0,       # the gridshell, overhanging 5.5 m each side
    "canopy_height_m": 4.5,
    "south_louvre_depth_m": 3.0,  # louvre blades on the southern edge
    "etfe_transmittance": 0.12,   # fraction of direct beam passing the infill
    "gate_sweep_deg": 4.0,        # angle at each end given to the arrival majlis
}

# ---------------------------------------------------------------------------
# Thermal comfort thresholds (NWS Heat Index bands, °C)
# ---------------------------------------------------------------------------
# Four bands, not five: they map one-to-one onto the four reserved status
# colours of the visual system. The NWS "Danger" and "Extreme Danger" bands are
# merged, because inventing a fifth status colour breaks the validated palette
# and the design response above 41 °C is identical either way — do not programme
# the space for use.
COMFORT_BANDS = [
    ("Comfortable", -100.0, 27.0),
    ("Caution", 27.0, 32.0),
    ("Extreme Caution", 32.0, 41.0),
    ("Danger", 41.0, 200.0),
]
COMFORT_ORDER = [b[0] for b in COMFORT_BANDS]

# Air-temperature relief measured under a shaded ETFE/tree canopy in hot-arid
# conditions. Applied to the exposed case to produce the shaded case.
SHADE_TEMP_RELIEF_C = 6.0
SHADE_MRT_RELIEF_C = 12.0  # mean radiant temperature relief, larger than air

# ---------------------------------------------------------------------------
# Machine learning
# ---------------------------------------------------------------------------
RANDOM_SEED = 42
TEST_SIZE = 0.15
VAL_SIZE = 0.15          # of the full set; train therefore = 0.70
CV_FOLDS = 5

# ---------------------------------------------------------------------------
# Visual design system
# ---------------------------------------------------------------------------
# ONE palette for every figure in the submission. Do not introduce a colour that
# is not in this block.
#
# These values are not a matter of taste — they were verified by running
# scripts/validate_palette.js, which computes colour-vision-deficiency
# separation in OKLab rather than judging it by eye. Results, against the
# surfaces below:
#
#   categorical light : ALL PASS  (worst adjacent CVD dE 9.1 protan,
#                                  worst adjacent normal-vision dE 19.6)
#   categorical dark  : ALL PASS  (worst adjacent CVD dE 8.4, contrast all >=3:1)
#   heat ramp         : ALL PASS  (monotone lightness, single hue 12 deg spread,
#                                  light end 2.10:1 against the surface)
#
# An earlier hand-picked "desert palette" FAILED three of these checks — two of
# its greens were 3.6 dE apart under protanopia, i.e. the same colour to a
# red-green colour-blind juror. If you change any hex here, re-run the validator
# before committing.

PALETTE = {
    "ink": "#0b0b0b",        # primary text
    "ink_secondary": "#52514e",
    "muted": "#898781",      # axis labels, captions
    "rule": "#e1e0d9",       # gridlines (hairline)
    "baseline": "#c3c2b7",   # axis / baseline
    "paper": "#FBFAF7",      # figure surface — warm off-white
    "canvas": "#FFFFFF",
}

# Ordered categorical ramp. Assign in this order and never cycle it: a series
# keeps its colour across every chart, so the eye can carry identity from one
# figure to the next. Past six series, fold the tail into "Other" or facet the
# chart — do not generate a seventh hue.
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]
SERIES_DARK = ["#3987e5", "#d95926", "#199e70", "#c98500", "#d55181", "#008300"]

# Reserved status colours — severity only, never used as a series colour.
# Always shipped with a visible text label, never carrying meaning by hue alone.
STATUS = {
    "good": "#0ca30c",
    "warning": "#fab219",
    "serious": "#ec835a",
    "critical": "#d03b3b",
}

# Comfort bands map one-to-one onto the status roles, everywhere, no exceptions.
COMFORT_COLORS = {
    "Comfortable": STATUS["good"],
    "Caution": STATUS["warning"],
    "Extreme Caution": STATUS["serious"],
    "Danger": STATUS["critical"],
}

# Sequential single-hue ramp for continuous heat / comfort surfaces.
# Light = cool, dark = hot. Monotone in lightness so it survives greyscale
# printing and colour-blind viewing.
HEAT_RAMP = ["#f19a68", "#e97b41", "#d0561f", "#a83e14", "#7f2c0e", "#571c08"]

SURFACE_LIGHT = "#FBFAF7"
SURFACE_DARK = "#1a1a19"

FIGURE = {
    "dpi": 200,
    "width_in": 10.0,
    "height_in": 5.6,
    "font_family": "DejaVu Sans",
    "title_size": 13,
    "label_size": 10,
    "tick_size": 9,
    "caption_size": 8,
}

PROJECT_STAMP = "Al Safa 2 Park · Falaj Al Safa · Dubai Municipality AI Design Challenge"

# ---------------------------------------------------------------------------
# Repository / publication
# ---------------------------------------------------------------------------
GITHUB_USER = "wasimmisaw437"
GITHUB_REPO = "al-safa-2-park-ai"
GITHUB_URL = f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}"
PAGES_URL = f"https://{GITHUB_USER}.github.io/{GITHUB_REPO}/"
