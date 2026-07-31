"""The submission's technical drawings, generated from the masterplan geometry.

Why this module exists
----------------------
The drawings that went into the previous submission were authored separately
from the analysis and then drifted away from it. By the end, the section showed
a 10 m walkway under a 5.5 m canopy with no louvre, the circulation diagram
claimed "100% shaded", and the planting plan drew rooms that the model no longer
had — three drawings, none of which described the scheme the numbers were about.

Every drawing here reads `src.plan` and `src.solar`. If the crescent's sagitta
changes, the section, the elevation, the circulation diagram and the planting
plan all change with it, or this module fails loudly. A drawing that can quietly
disagree with the model is worse than no drawing.

    python -m src.drawings          writes design/visuals/
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from matplotlib.patches import Circle, Ellipse, Polygon, Rectangle

from . import config as C, plan, solar, viz

OUT = C.ROOT / "design" / "visuals"

# Sun angles are computed, not remembered. These are noon at the two solstices
# for the real site coordinates, straight out of the NREL algorithm.
_SOL = None


def solstice_angles() -> dict:
    global _SOL
    if _SOL is None:
        s = solar.hourly_solar_position()
        out = {}
        for month, day, key in ((6, 21, "summer"), (12, 21, "winter")):
            d = s[(s.index.month == month) & (s.index.day == day)]
            n = d.loc[d["elevation_deg"].idxmax()]
            out[key] = (float(n["elevation_deg"]), float(n["azimuth_deg"]))
        _SOL = out
    return _SOL


def _site_frame(ax, *, north=True, scale=True):
    """Site boundary, north point and a graphic scale bar."""
    ax.add_patch(Polygon([(0, 0), (C.SITE["length_m"], 0),
                          (C.SITE["length_m"], C.SITE["width_m"]),
                          (0, C.SITE["width_m"])], closed=True, fill=False,
                         edgecolor=C.PALETTE["ink"], linewidth=1.4, zorder=20))
    if north:
        ax.annotate("N", xy=(145, 96), ha="center", va="center", fontsize=10,
                    fontweight="semibold", color=C.PALETTE["ink_secondary"], zorder=21)
        ax.annotate("", xy=(145, 94), xytext=(145, 84), zorder=21,
                    arrowprops=dict(arrowstyle="<|-", lw=1.2,
                                    color=C.PALETTE["ink_secondary"]))
    if scale:
        ax.plot([6, 26], [-6.5, -6.5], color=C.PALETTE["ink"], lw=2.2, zorder=21,
                clip_on=False, solid_capstyle="butt")
        ax.text(16, -9.0, "20 m", ha="center", va="top", fontsize=8,
                color=C.PALETTE["muted"], clip_on=False)
    ax.set_xlim(-6, C.SITE["length_m"] + 6)
    ax.set_ylim(-13, C.SITE["width_m"] + 6)
    ax.set_aspect("equal")
    ax.axis("off")


def _ground(ax, zones, *, fill=None, edge=None):
    """Wash every room in as a recessive base for an overlay drawing."""
    for z in zones:
        for part in z["parts"]:
            if len(part) >= 3:
                ax.add_patch(Polygon(part, closed=True,
                                     facecolor=fill or C.PALETTE["rule"], alpha=0.45,
                                     edgecolor=edge or C.PALETTE["baseline"],
                                     linewidth=0.6, zorder=1))


# ---------------------------------------------------------------------------
# 1. Section through the crescent
# ---------------------------------------------------------------------------
def section():
    """Section A-A, cut radially across the crescent at midspan.

    This is the drawing the whole scheme rests on, so every dimension in it is
    read from config.CRESCENT and every sun ray from the solar model.
    """
    cr = C.CRESCENT
    pw, cw = cr["path_width_m"], cr["canopy_width_m"]
    h, ld = cr["canopy_height_m"], cr["south_louvre_depth_m"]
    # The shell springs at CRESCENT.canopy_height_m and vaults ABOVE it. The
    # shade model treats the canopy as a horizontal plane at the springing, so
    # taking the springing as the datum keeps the drawing conservative against
    # the model rather than flattering it — the real shell shades slightly more
    # than the number claims, never less.
    spring, crown = h, h + 1.2
    ang = solstice_angles()

    fig, ax = viz.open_figure(
        "Section A–A — the Crescent Canopy at midspan",
        f"Every dimension read from config.CRESCENT; sun angles computed by the "
        f"NREL algorithm at {C.SITE['latitude']:.3f}°N",
        width=12.0, height=6.0,
    )

    # Ground, walk and the two planted margins. +x is SOUTH in this section.
    ax.add_patch(Rectangle((-cw / 2 - 6, -1.2), cw + 12, 1.2,
                           facecolor=C.PALETTE["rule"], edgecolor="none", zorder=1))
    ax.plot([-cw / 2 - 6, cw / 2 + 6], [0, 0], color=C.PALETTE["ink"], lw=1.4, zorder=3)
    ax.add_patch(Rectangle((-pw / 2, 0), pw, 0.12, facecolor=C.SERIES[0],
                           edgecolor="none", alpha=0.8, zorder=4))

    # Al Falaj — a 0.9 m channel sunk into the northern margin, under the
    # canopy's drip line. Drawn where the plan puts it, not where it looks best.
    fx = plan.FALAJ_OFFSET_M + plan.FALAJ_WIDTH_M / 2.0
    ax.add_patch(Rectangle((fx - plan.FALAJ_WIDTH_M / 2, -0.55),
                           plan.FALAJ_WIDTH_M, 0.55, facecolor=C.SERIES[2],
                           alpha=0.85, edgecolor=C.SERIES[2], zorder=5))
    ax.annotate("Al Falaj — 0.9 m channel, set on the\ncanopy's drip line so it "
                "is shaded all day.\nAn open channel here evaporates.",
                xy=(fx, -0.55), xytext=(-cw / 2 - 6.5, 6.6), fontsize=7.5,
                ha="left", va="top", color=C.SERIES[2], linespacing=1.35,
                arrowprops=dict(arrowstyle="-", lw=0.8, color=C.SERIES[2]))

    # The gridshell: a shallow vault, crowning over the walk.
    u = np.linspace(0, 1, 160)
    gx = (u - 0.5) * cw
    gy = spring + (crown - spring) * np.sin(np.pi * u)
    ax.plot(gx, gy, color=C.PALETTE["ink"], lw=2.6, zorder=8, solid_capstyle="round")
    ax.fill_between(gx, gy, gy + 0.28, color=C.PALETTE["ink"], alpha=0.18, zorder=7)

    # Columns at the two springings, and the southern louvre blade.
    for sx in (-cw / 2, cw / 2):
        ax.plot([sx, sx], [0, spring], color=C.PALETTE["ink"], lw=2.4, zorder=8)
    for i in range(8):
        yb = spring - ld * (i + 0.5) / 8
        ax.plot([cw / 2 - 0.62, cw / 2 + 0.12], [yb + 0.26, yb], color=C.SERIES[1],
                lw=1.3, zorder=9, solid_capstyle="round")
    ax.annotate(f"{ld:.0f} m southern louvre — the piece\nthat buys the winter. "
                f"A mashrabiya's\nlogic: a deep screen on the face\nthe sun "
                f"comes from.",
                xy=(cw / 2 + 0.1, spring - ld / 2), xytext=(cw / 2 + 3.4, -1.2),
                fontsize=7.5, ha="left", va="top", color=C.SERIES[1],
                linespacing=1.35,
                arrowprops=dict(arrowstyle="-", lw=0.8, color=C.SERIES[1]))

    # The tree avenue at mature canopy. Ghaf on the south rank, Neem on the
    # north. Drawn behind the structure and in outline: at true size a mature
    # Ghaf crown is 12 m across and a solid fill hides the very section this
    # drawing exists to show. They really do knit into the overhang — that is
    # the intent, not an error in the drawing.
    for sgn, name, r, th in ((1, "Ghaf", 6.0, 8.0), (-1, "Neem", 5.0, 9.0)):
        tx = sgn * (pw + cw) / 4.0
        cy = th * 0.66
        ax.plot([tx, tx], [0, cy], color="#6b5a44", lw=2.0, zorder=2)
        ax.add_patch(Ellipse((tx, cy), 2 * r, th * 0.62, facecolor=C.SERIES[5],
                             alpha=0.11, edgecolor=C.SERIES[5], lw=0.9, zorder=2))
        ax.text(tx, -1.55, f"{name} · {r * 2:.0f} m crown at maturity",
                ha="center", fontsize=7.5, color=C.PALETTE["ink_secondary"])

    # A person, for scale. 1.75 m.
    ax.plot([1.6, 1.6], [0, 1.45], color=C.PALETTE["ink_secondary"], lw=1.6, zorder=6)
    ax.add_patch(Circle((1.6, 1.62), 0.16, facecolor=C.PALETTE["ink_secondary"],
                        edgecolor="none", zorder=6))
    ax.text(2.3, 0.85, "1.75 m", fontsize=7, color=C.PALETTE["muted"], va="center")

    # Sun rays at both solstices, at their computed noon elevations. The two
    # rays are struck from different points so their labels do not collide, and
    # each is aimed at the edge of the structure it is actually tested against:
    # the June sun at the crown, the December sun at the louvre's bottom edge.
    for key, colour, label, target, y0 in (
        ("summer", C.STATUS["critical"], "June solstice noon", (0.0, crown + 0.3), 12.6),
        ("winter", C.SERIES[0], "December solstice noon",
         (cw / 2, spring - ld), 9.4),
    ):
        elev = ang[key][0]
        a = np.radians(elev)
        tx, ty = target
        x0 = tx + (y0 - ty) / np.tan(a)
        ax.annotate("", xy=(tx, ty), xytext=(x0, y0), zorder=10,
                    arrowprops=dict(arrowstyle="-|>", lw=1.3, color=colour))
        ax.text(x0 + 0.4, y0 + 0.25, f"{label} · {elev:.1f}°", fontsize=7.5,
                color=colour, va="bottom", ha="left")

    # Dimensions.
    def dim(x0, x1, y, text):
        ax.annotate("", xy=(x0, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle="<|-|>", lw=0.9,
                                    color=C.PALETTE["ink_secondary"]))
        ax.text((x0 + x1) / 2, y - 0.30, text, ha="center", va="top",
                fontsize=7.5, color=C.PALETTE["ink_secondary"])

    dim(-pw / 2, pw / 2, -2.6, f"{pw:.0f} m walk")
    dim(-cw / 2, cw / 2, -3.9, f"{cw:.0f} m gridshell — overhangs "
                               f"{(cw - pw) / 2:.1f} m each side")
    ax.annotate("", xy=(cw / 2 + 2.4, 0), xytext=(cw / 2 + 2.4, h),
                arrowprops=dict(arrowstyle="<|-|>", lw=0.9,
                                color=C.PALETTE["ink_secondary"]))
    ax.text(cw / 2 + 2.8, spring / 2, f"{spring:.1f} m to the shading plane",
            rotation=90, ha="left",
            va="center", fontsize=7.5, color=C.PALETTE["ink_secondary"])

    ax.text(-cw / 2 - 6.5, 0.35, "NORTH\n(concave — the cool side)", fontsize=7.5,
            va="bottom", color=C.PALETTE["muted"], linespacing=1.3)
    ax.text(cw / 2 + 16.5, 0.35, "SOUTH\n(convex)", fontsize=7.5, va="bottom",
            ha="right", color=C.PALETTE["muted"], linespacing=1.3)

    ax.set_xlim(-cw / 2 - 7, cw / 2 + 17)
    ax.set_ylim(-5.0, 13.8)
    ax.set_aspect("equal")
    ax.axis("off")

    return viz.finish(
        fig, "section_crescent", save_to=OUT,
        source="src/config.py CRESCENT; sun angles NREL SPA via pvlib",
        note="The plane alone loses the walk to a low southern sun. The louvre "
             "is what holds the shadow on the path from November to January.",
    )


# ---------------------------------------------------------------------------
# 2. Long elevation
# ---------------------------------------------------------------------------
def elevation():
    """The crescent seen along its length — the bay rhythm and the horns."""
    cr = C.CRESCENT
    h = cr["canopy_height_m"]
    spring, crown = h, h + 1.2      # same datum as the section, see above
    bay = 6.0
    run = 60.0

    fig, ax = viz.open_figure(
        "Elevation — the Crescent Canopy",
        f"{run:.0f} m of the {plan.ARC_R * 2 * np.radians(plan.WALK_THETA):.0f} m "
        f"run, to scale. 6 m structural bay",
        width=12.0, height=4.4,
    )
    # Trees first, behind everything, in outline. At true mature size a solid
    # fill would bury the structure this drawing is about.
    rng = np.random.default_rng(C.RANDOM_SEED)
    for i in range(10):
        tx = 1.5 + i * (run - 3) / 9 + rng.uniform(-0.9, 0.9)
        th, r = (9.0, 5.0) if i % 2 else (8.0, 6.0)
        cy = th * 0.66
        ax.plot([tx, tx], [0, cy], color="#6b5a44", lw=1.6, zorder=2)
        ax.add_patch(Ellipse((tx, cy), 2 * r, th * 0.62, facecolor=C.SERIES[5],
                             alpha=0.10, edgecolor=C.SERIES[5], lw=0.8, zorder=2))

    ax.plot([-2, run + 2], [0, 0], color=C.PALETTE["ink"], lw=1.4, zorder=5)

    # The shell is a run of transverse arches. Seen from the side you read the
    # near springing line, the crown line behind it, and the ribs between —
    # which is what gives the structure its rhythm, so it is drawn rather than
    # flattened into a grey band.
    n_bay = int(run / bay)
    for i in range(n_bay + 1):
        x = i * bay
        ax.plot([x, x], [0, spring], color=C.PALETTE["ink"], lw=2.6, zorder=6)
        # The rib, foreshortened: it springs at this bay and crowns 4 m "behind".
        u = np.linspace(0, 1, 40)
        ax.plot(x + 2.9 * u, spring + (crown - spring) * np.sin(np.pi * u / 2),
                color=C.PALETTE["ink"], lw=1.0, alpha=0.45, zorder=6)

    ax.plot([0, run], [spring, spring], color=C.PALETTE["ink"], lw=2.2, zorder=7)
    ax.plot([2.9, run + 2.9], [crown, crown], color=C.PALETTE["ink"], lw=1.2,
            alpha=0.45, zorder=6)

    # The perforated soffit between springing and crown: a rhythm of openings,
    # not a slab. 12% of the direct beam passes.
    ax.add_patch(Rectangle((0, spring), run, 0.55, facecolor=C.PALETTE["ink"],
                           alpha=0.16, edgecolor="none", zorder=6))
    for i in range(int(run / 0.9)):
        x = 0.45 + i * 0.9
        if x < run:
            ax.plot([x, x], [spring + 0.08, spring + 0.47], color=C.PALETTE["paper"],
                    lw=1.5, zorder=7)
    ax.annotate("Perforated soffit — 12% direct-beam transmittance.\n"
                "The mashrabiya rule: light through, heat stopped.",
                xy=(run * 0.30, spring + 0.55), xytext=(run * 0.30, crown + 3.0),
                fontsize=7.5, ha="center", color=C.PALETTE["ink_secondary"],
                linespacing=1.35,
                arrowprops=dict(arrowstyle="-", lw=0.8, color=C.PALETTE["baseline"]))

    # The southern louvre, seen face-on: a hanging screen of vertical blades.
    ld = cr["south_louvre_depth_m"]
    ax.add_patch(Rectangle((0, spring - ld), run, ld, facecolor=C.SERIES[1],
                           alpha=0.13, edgecolor="none", zorder=4))
    for i in range(int(run / 0.75)):
        x = 0.375 + i * 0.75
        if x < run:
            ax.plot([x, x], [spring - ld, spring], color=C.SERIES[1], lw=0.7,
                    alpha=0.55, zorder=4)
    ax.annotate(f"{ld:.0f} m southern louvre",
                xy=(run * 0.80, spring - ld / 2), xytext=(run * 0.80, -2.9),
                fontsize=7.5, ha="center", va="top", color=C.SERIES[1],
                arrowprops=dict(arrowstyle="-", lw=0.8, color=C.SERIES[1]))

    ax.plot([1.2, 1.2], [0, 1.45], color=C.PALETTE["ink_secondary"], lw=1.5, zorder=8)
    ax.add_patch(Circle((1.2, 1.62), 0.16, facecolor=C.PALETTE["ink_secondary"],
                        edgecolor="none", zorder=8))

    ax.annotate("", xy=(0, -1.5), xytext=(bay, -1.5),
                arrowprops=dict(arrowstyle="<|-|>", lw=0.9,
                                color=C.PALETTE["ink_secondary"]))
    ax.text(bay / 2, -2.1, f"{bay:.0f} m bay", ha="center", va="top", fontsize=7.5,
            color=C.PALETTE["ink_secondary"])

    ax.set_xlim(-3, run + 5)
    ax.set_ylim(-5.4, 13.0)
    ax.set_aspect("equal")
    ax.axis("off")

    n_total = int(np.ceil(plan.ARC_R * 2 * np.radians(plan.WALK_THETA) / bay))
    return viz.finish(
        fig, "elevation_crescent", save_to=OUT,
        source="src/config.py CRESCENT; bay spacing from the Phase 6 structure",
        note=f"{n_total} bays over the full run. Because the plan is an arc, no "
             f"two bays are identical in plan — but every one is the same "
             f"section, which is what keeps it buildable. Trees at mature canopy "
             f"from the Phase 6 planting schedule.",
    )


# ---------------------------------------------------------------------------
# 3. Circulation and accessibility
# ---------------------------------------------------------------------------
def circulation():
    """How the park is entered, crossed and circled."""
    zones = plan.build()
    fig, ax = viz.open_figure(
        "Circulation & accessibility",
        "One shaded primary route, radial alleys off it, and a running loop "
        "around the whole",
        width=10.6, height=7.6,
    )
    _ground(ax, [z for z in zones if not z.get("is_residual")])

    sx, sy, _, _ = plan.centreline(300)
    ax.plot(sx, sy, color=C.SERIES[0], lw=C.CRESCENT["path_width_m"] * 1.0,
            solid_capstyle="round", alpha=0.85, zorder=6,
            label="Al Mamsha — primary route, shaded, step-free")

    first = True
    for seg in plan.sikka_lines():
        ax.plot(seg[:, 0], seg[:, 1], color=C.SERIES[3], lw=2.2, zorder=5,
                linestyle=(0, (1, 1.6)), solid_capstyle="round",
                label="Al Sikkak — shaded alleys to the rooms" if first else None)
        first = False

    lx, ly = plan.loop_polyline()
    ax.plot(lx, ly, color=C.SERIES[2], lw=2.4, zorder=5,
            label=f"Al Madar — {_loop_length(lx, ly):.0f} m running loop")

    # Service and emergency access: in at the east gate, along the southern
    # margin, out again. Kept off the walk, which is why it is drawn.
    ex, ey, _, _ = plan.centreline(160, d_m=C.CRESCENT["canopy_width_m"] / 2 + 3.0)
    ax.plot(ex, ey, color=C.STATUS["critical"], lw=1.6, zorder=5,
            linestyle=(0, (7, 3)), label="Service / emergency vehicle access")

    for z in zones:
        if z["key"] in ("gate_w", "gate_e"):
            gx, gy = z["label_xy"]
            ax.add_patch(Circle((gx, gy), 4.2, facecolor=C.STATUS["warning"],
                                alpha=0.85, edgecolor="none", zorder=8))
            ax.annotate(z["name"].replace(" Majlis", "\nMajlis"),
                        xy=(np.clip(gx, 16, C.SITE["length_m"] - 16), gy - 6.5),
                        ha="center", va="top", fontsize=8, zorder=9,
                        color=C.PALETTE["ink_secondary"], linespacing=1.3)
    for pod in plan.majlis_pods():
        ax.add_patch(Circle((pod["x"], pod["y"]), pod["r"], facecolor="none",
                            edgecolor=C.SERIES[4], lw=1.4, zorder=7))

    # How far you can be on the walk from the nearest shaded pavilion. Measured
    # along the drawn route, not asserted: the number below moves if the alley
    # partition in src/plan.py moves.
    wx, wy, _, _ = plan.centreline(400)
    pods = plan.majlis_pods()
    to_pod = np.sqrt(np.min([(wx - p["x"]) ** 2 + (wy - p["y"]) ** 2
                             for p in pods], axis=0))
    ax.scatter([], [], s=60, facecolor="none", edgecolor=C.SERIES[4],
               label=f"Majlis — shaded rest, never more than "
                     f"{np.ceil(to_pod.max()):.0f} m from the walk")

    _site_frame(ax)
    ax.legend(loc="upper center", ncol=2, bbox_to_anchor=(0.5, -0.02),
              handlelength=2.4, columnspacing=2.0)

    return viz.finish(
        fig, "circulation_crescent", save_to=OUT,
        source="src/plan.py — routes are the drawn geometry, not a sketch over it",
        note="Every room is reached from the shaded route by one alley. The site "
             "is level, so the whole park is step-free; the only change of level "
             "in the scheme is the Oasis Basin, which is ramped.",
    )


def _loop_length(x, y) -> float:
    return float(np.hypot(np.diff(x), np.diff(y)).sum())


# ---------------------------------------------------------------------------
# 4. Planting plan
# ---------------------------------------------------------------------------
def planting():
    """The 131 trees at mature canopy, on the rooms the plan gives them."""
    trees = solar.tree_positions()
    species = pd.read_csv(C.DATA_RAW / "species_water_carbon_rates.csv")
    zones = plan.build()

    fig, ax = viz.open_figure(
        "Planting plan — 131 trees",
        "Drawn at mature canopy radius. The avenue is structural: it carries the "
        "shoulder seasons the gridshell cannot",
        width=10.6, height=7.8,
    )
    _ground(ax, [z for z in zones if not z.get("is_residual")])
    ax.add_patch(Polygon(plan.canopy_outline(), closed=True, facecolor=C.SERIES[0],
                         alpha=0.13, edgecolor="none", zorder=2))

    colours = {"Ghaf": C.SERIES[5], "Neem": C.SERIES[2], "Ficus nitida": C.SERIES[4],
               "Olive": C.SERIES[3], "Date Palm": C.SERIES[1]}
    order = ["Ghaf", "Neem", "Ficus nitida", "Olive", "Date Palm"]
    info = species.set_index("Species")

    for name in order:
        sub = trees[trees["species"] == name]
        for _, t in sub.iterrows():
            ax.add_patch(Circle((t["x"], t["y"]), t["canopy_r_m"],
                                facecolor=colours[name], alpha=0.22,
                                edgecolor="none", zorder=3))
        ax.scatter(sub["x"], sub["y"], s=8, color=colours[name], linewidths=0,
                   zorder=6,
                   label=f"{name} ({info.loc[name, 'ScientificName']}) ×{len(sub)}"
                         f" · {info.loc[name, 'Water_L_per_tree_day_summer']:.0f} L/day")

    _site_frame(ax)
    ax.legend(loc="upper center", ncol=2, bbox_to_anchor=(0.5, -0.02),
              columnspacing=2.0, handletextpad=0.5)

    native = int(species.loc[species["Native"] == 1, "Count"].sum())
    water = float((species["Count"] * species["Water_L_per_tree_day_summer"]).sum())
    return viz.finish(
        fig, "planting_crescent", save_to=OUT,
        source="data/raw/species_water_carbon_rates.csv; layout from src/solar.py",
        note=f"{native} of 131 trees are UAE natives (Ghaf and Date Palm). Peak "
             f"summer irrigation demand {water / 1000:.1f} m³/day. Ghaf takes the "
             f"southern rank because it is the most drought-tolerant species in "
             f"the schedule and that rank is the more exposed of the two.",
    )


# ---------------------------------------------------------------------------
def build_all() -> list:
    viz.apply_style()
    OUT.mkdir(parents=True, exist_ok=True)
    return [section(), elevation(), circulation(), planting()]


if __name__ == "__main__":
    for p in build_all():
        print(p)
