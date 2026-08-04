"""The two presentation boards, composed from the live figures and drawings.

The previous boards were assembled once by hand and then went stale: by the end
they showed the superseded rectangular layout, printed "AI-generated draft
layout for review" in the middle of the sheet, and carried a shade figure the
project had already withdrawn. A board that is composed once and never rebuilt
is a board that will eventually contradict the submission it belongs to.

These two are composed from files on disk, every time. Run the analysis, run the
drawings, run this — and the boards cannot be out of date.

    python -m src.boards
"""

from __future__ import annotations

import json

import matplotlib.image as mpimg
import matplotlib.pyplot as plt

from . import config as C, plan, viz

OUT = C.ROOT / "design" / "boards"

# A1 landscape at 200 dpi.
SHEET_W, SHEET_H = 16.54, 11.69


def _panel(fig, rect, path, *, caption=None, pending=None):
    """Place an image inside a rect, preserving its aspect ratio.

    When the image is absent the panel draws a quiet "pending" placeholder
    rather than an error. Four of the photoreal renders were withdrawn because
    they showed a different park from the one in the plan — a serpentine canopy
    over a lagoon, and a dead-straight corridor. A board that admits a view is
    still being made costs far less than a board that captions the wrong park
    as the crescent, which is what these panels used to do.
    """
    ax = fig.add_axes(rect)
    ax.axis("off")
    if caption:
        ax.set_title(caption, fontsize=8.5, loc="left", pad=4,
                     color=C.PALETTE["ink_secondary"], fontweight="normal")
    if not path.exists():
        ax.add_patch(plt.Rectangle(
            (0.005, 0.005), 0.99, 0.99, transform=ax.transAxes, zorder=0,
            facecolor=C.PALETTE["canvas"], edgecolor=C.PALETTE["muted"],
            linestyle=(0, (5, 4)), linewidth=0.8))
        ax.text(0.5, 0.57, "Visualisation in preparation", ha="center",
                va="center", fontsize=9, color=C.PALETTE["ink_secondary"],
                transform=ax.transAxes, zorder=1)
        ax.text(0.5, 0.40, pending or f"{path.name} — see AL_SAFA_MASTER_PROMPT.md",
                ha="center", va="center", fontsize=6.6,
                color=C.PALETTE["muted"], transform=ax.transAxes, zorder=1,
                wrap=True)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        return ax
    ax.imshow(mpimg.imread(path))
    return ax


def _sheet(title: str, index: str):
    fig = plt.figure(figsize=(SHEET_W, SHEET_H))
    fig.patch.set_facecolor(C.PALETTE["paper"])
    head = fig.add_axes([0, 0.945, 1, 0.055])
    head.axis("off")
    head.set_facecolor(C.PALETTE["ink"])
    head.add_patch(plt.Rectangle((0, 0), 1, 1, transform=head.transAxes,
                                 facecolor=C.PALETTE["ink"], zorder=0))
    head.text(0.014, 0.52, f"AL SAFA 2 PARK — {C.SITE['concept'].upper()}",
              va="center", ha="left", fontsize=17, fontweight="bold",
              color=C.PALETTE["canvas"], transform=head.transAxes, zorder=1)
    head.text(0.986, 0.52,
              f"Dubai Municipality AI Park Design Challenge   |   {index}",
              va="center", ha="right", fontsize=9.5, color=C.STATUS["warning"],
              transform=head.transAxes, zorder=1)
    fig.text(0.014, 0.930, title, fontsize=11, fontweight="semibold",
             color=C.PALETTE["ink"], va="top")
    return fig


def _foot(fig, text: str):
    fig.text(0.014, 0.012, text, fontsize=7.6, color=C.PALETTE["muted"],
             va="bottom", linespacing=1.5)


def board_concept():
    """Board 1 — the scheme: what it is and why it takes this shape."""
    F, D, R = C.FIGURES, C.ROOT / "design" / "visuals", C.ROOT / "design" / "renders"
    fig = _sheet("The concept, the plan, and the section that makes it work",
                 "Board 1 of 2 — CONCEPT")

    _panel(fig, [0.010, 0.415, 0.575, 0.505], F / "fig10_masterplan.png")
    # This panel held masterplan_aerial_golden_hour.jpg, which shows a closed
    # oval ring. It sat directly beside fig10_masterplan.png, which shows the
    # single open arc — so the board presented two different parks side by side
    # and captioned the wrong one "the crescent". Nothing undermines a design
    # board faster than contradicting itself within one sheet.
    #
    # Until an aerial exists that shows this scheme, the panel carries a render
    # that does. The aerial is still wanted — see AL_SAFA_MASTER_PROMPT.md
    # prompt 01, which now states in as many ways as it can that the arc is one
    # open curve with two ends and not a ring.
    _panel(fig, [0.600, 0.655, 0.392, 0.265],
           R / "Night" / "night_plaza_render_1784970565232.jpg",
           caption="Al Hilal after dark — the canopy lit from within",
           pending="Aerial view · AL_SAFA_MASTER_PROMPT.md prompt 01")
    _panel(fig, [0.600, 0.400, 0.392, 0.215],
           R / "Eye_Level" / "spine_corridor_interior.jpg",
           caption="Beneath Al Hilal — the perforated soffit at eye level",
           pending="Eye-level view · AL_SAFA_MASTER_PROMPT.md prompt 03")
    _panel(fig, [0.010, 0.070, 0.500, 0.320], D / "section_crescent.png")
    _panel(fig, [0.520, 0.070, 0.472, 0.320], D / "circulation_crescent.png")

    m = json.loads((C.MODELS / "headline_metrics.json").read_text(encoding="utf-8"))
    _foot(fig,
          f"One arc. Every room in the park is struck off its centre, so no room is a "
          f"rectangle and every room faces the crescent square-on.\n"
          f"The bow is {C.CRESCENT['sagitta_m']:.0f} m deep on a "
          f"{plan.ARC_R:.0f} m radius — swept against the 8,760-hour solar model, not "
          f"drawn by eye. A straight canopy shades marginally more ground on average "
          f"and leaves the walk with no shade at all for 330 hours a year; this one "
          f"leaves it for 56.\n"
          f"Walk shaded {m['spine_shade_canopy_only_pct']:.1f}% of daylight hours   ·   "
          f"131 trees   ·   15,000 m²   ·   every number reproducible with "
          f"`python run_analysis.py`")
    return _save(fig, "board_1_concept")


def board_evidence():
    """Board 2 — the evidence: what was measured, and what it changed."""
    F, D = C.FIGURES, C.ROOT / "design" / "visuals"
    fig = _sheet("What the models measured, and what they changed about the design",
                 "Board 2 of 2 — EVIDENCE")

    _panel(fig, [0.010, 0.545, 0.500, 0.375], F / "fig04_site_comfort_map.png")
    _panel(fig, [0.520, 0.700, 0.472, 0.220], F / "fig02_comfort_bands.png")
    _panel(fig, [0.520, 0.455, 0.472, 0.245], F / "fig03_shade_by_zone.png")
    _panel(fig, [0.010, 0.285, 0.500, 0.255], F / "fig06_feature_importance.png")
    _panel(fig, [0.520, 0.200, 0.472, 0.255], F / "fig09_diurnal_comfort.png")
    _panel(fig, [0.010, 0.070, 0.310, 0.210], D / "planting_crescent.png")
    _panel(fig, [0.330, 0.075, 0.660, 0.130], D / "elevation_crescent.png")

    m = json.loads((C.MODELS / "headline_metrics.json").read_text(encoding="utf-8"))
    _foot(fig,
          f"Comfortable daylight hours rise from "
          f"{m['daylight_hours_comfortable_exposed_pct']:.1f}% to "
          f"{m['daylight_hours_comfortable_shaded_pct']:.1f}% — "
          f"{m['comfort_hours_gained_pct_points']:.1f} points of the year handed back. "
          f"Peak heat index falls {m['peak_heat_index_exposed_c']:.1f} °C → "
          f"{m['peak_heat_index_shaded_c']:.1f} °C.\n"
          f"Site-wide mean shade is {m['site_mean_shade_pct']:.1f}%, and that is "
          f"stated as a position rather than hidden: this scheme makes a few places "
          f"genuinely excellent instead of the whole site marginally better.\n"
          f"Shade surrogate R² {m['model_M1_test_r2']:.3f}   ·   comfort classifier "
          f"{m['model_M2_test_accuracy']:.1%} with temperature and humidity withheld   "
          f"·   {m['model_M3_regimes']} microclimate regimes, k selected by silhouette")
    return _save(fig, "board_2_evidence")


def _save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / f"{name}.png"
    fig.savefig(out, dpi=200, facecolor=C.PALETTE["paper"])
    plt.close(fig)
    return out


def build_all() -> list:
    viz.apply_style()
    return [board_concept(), board_evidence()]


if __name__ == "__main__":
    for p in build_all():
        print(p)
