"""
Every figure in the submission, generated from the analysis outputs.

One module, one visual system. A figure that is not produced here does not
appear in the submission, which is what stops the deck drifting back into a
collection of mismatched images.

Rules applied throughout, from the project's data-visualisation standard:
  * no dual y-axes anywhere — two scales become two stacked panels
  * colours only from the validated palette in config.py
  * a legend whenever two or more series are present, plus direct labels
  * a source line on every figure
  * sequential single-hue ramp for continuous surfaces, status colours for bands
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from matplotlib.patches import Circle, Rectangle

from . import config as C, viz

NCM = "NCM Dubai climate normals 1977-2015 (39-year record)"
SPA = "NREL Solar Position Algorithm via pvlib, 25.190N 55.238E"
MODEL = "This project's models — see notebooks/ and src/"


# ---------------------------------------------------------------------------
def fig_climate_profile(normals: pd.DataFrame, hourly: pd.DataFrame):
    """Monthly temperature and heat index. Two panels, never two y-axes."""
    fig, (ax1, ax2) = viz.stacked_panels(
        "Dubai climate and what it feels like",
        "Monthly normals against the modelled heat index, exposed and shaded",
        ratios=(1.1, 1),
    )
    m = normals["Month"]

    ax1.plot(m, normals["TempMax_C"], color=C.SERIES[1], marker="o", label="Mean daily max")
    ax1.plot(m, normals["TempAvg_C"], color=C.SERIES[0], marker="o", label="Mean")
    ax1.plot(m, normals["TempMin_C"], color=C.SERIES[2], marker="o", label="Mean daily min")
    ax1.set_ylabel("Air temperature (°C)")
    ax1.legend(loc="upper left", ncol=3)

    mon = hourly.groupby(hourly.index.month)
    hi_ex = mon["heat_index_c"].max()
    hi_sh = mon["heat_index_shaded_c"].max()
    ax2.plot(m, hi_ex.to_numpy(), color=C.SERIES[3], marker="s", label="Exposed — peak heat index")
    ax2.plot(m, hi_sh.to_numpy(), color=C.SERIES[0], marker="s", label="Under canopy shade")
    ax2.fill_between(range(12), hi_sh.to_numpy(), hi_ex.to_numpy(),
                     color=C.SERIES[3], alpha=0.12, linewidth=0)
    ax2.axhline(32, color=C.PALETTE["muted"], linestyle="--", linewidth=1)
    ax2.annotate("32 °C — comfort threshold", xy=(0.2, 32), xytext=(0, 0.4),
                 textcoords="offset fontsize", fontsize=8, color=C.PALETTE["muted"])
    ax2.set_ylabel("Peak heat index (°C)")
    ax2.legend(loc="upper left", ncol=2)

    return viz.finish(
        fig, "fig01_climate_and_comfort",
        source=f"{NCM}; heat index MODELLED (NWS Rothfusz)",
        note="Shaded case applies a 6 °C air-temperature relief with the "
             "resulting humidity rise computed, not assumed.",
    )


def fig_comfort_bands(hourly: pd.DataFrame):
    """How much of the year is usable, exposed versus shaded."""
    day = hourly[hourly["is_daylight"]]
    ex = day["comfort_band"].value_counts(normalize=True).reindex(C.COMFORT_ORDER).fillna(0) * 100
    sh = day["comfort_band_shaded"].value_counts(normalize=True).reindex(C.COMFORT_ORDER).fillna(0) * 100

    fig, ax = viz.open_figure(
        "Shade converts unusable daylight hours into usable ones",
        "Share of the year's 4,402 daylight hours in each comfort band",
        height=4.2,
    )
    left_ex = left_sh = 0.0
    for band in C.COMFORT_ORDER:
        b1 = ax.barh("Exposed", ex[band], left=left_ex, color=C.COMFORT_COLORS[band], label=band)
        b2 = ax.barh("With shade", sh[band], left=left_sh, color=C.COMFORT_COLORS[band])
        viz.bar_gap_style(list(b1) + list(b2))
        for val, left, row in ((ex[band], left_ex, 0), (sh[band], left_sh, 1)):
            if val >= 6:
                ax.text(left + val / 2, row, f"{val:.0f}%", ha="center", va="center",
                        fontsize=9, fontweight="semibold", color="white")
        left_ex += ex[band]
        left_sh += sh[band]

    ax.set_xlim(0, 100)
    ax.set_xlabel("Share of daylight hours (%)")
    ax.grid(axis="y", visible=False)
    viz.comfort_legend(ax, loc="lower center")
    ax.legend_.set_bbox_to_anchor((0.5, -0.42))

    return viz.finish(
        fig, "fig02_comfort_bands",
        source=f"{NCM}; comfort bands DERIVED via NWS heat index",
    )


def fig_shade_performance(grid: pd.DataFrame, hourly: pd.DataFrame):
    """Where the shade actually lands, by zone."""
    z = (grid.groupby("category")["shade_pct"].mean().sort_values(ascending=True))
    fig, ax = viz.open_figure(
        "Annual shade coverage by zone type",
        "Ray-traced ground-plane occlusion, 1 m grid, sampled across the year",
        height=4.6,
    )
    bars = ax.barh(z.index, z.to_numpy(), color=C.SERIES[0])
    viz.bar_gap_style(bars)
    for i, v in enumerate(z.to_numpy()):
        ax.text(v + 1.0, i, f"{v:.0f}%", va="center", fontsize=9,
                fontweight="semibold", color=C.PALETTE["ink_secondary"])
    ax.set_xlabel("Mean annual shade coverage (%)")
    ax.set_xlim(0, max(z.max() * 1.18, 10))
    ax.grid(axis="y", visible=False)

    return viz.finish(
        fig, "fig03_shade_by_zone",
        source=f"{SPA}; canopy and tree geometry from the Phase 5/6 design",
    )


def fig_site_comfort_map(grid: pd.DataFrame, trees: pd.DataFrame):
    """The design deliverable: predicted comfort, square metre by square metre."""
    fig, ax = viz.open_figure(
        "Predicted summer comfort across the site",
        "July afternoon heat index per square metre — the shade strategy, tested",
        width=11.0, height=6.4,
    )
    piv = grid.pivot_table(index="y", columns="x", values="summer_heat_index_c")
    im = ax.imshow(
        piv.to_numpy(), origin="lower", cmap=viz.HEAT_CMAP, aspect="equal",
        extent=(0, C.SITE["length_m"], 0, C.SITE["width_m"]),
    )
    # Trunk positions only. Drawing 131 mature canopy circles at true radius
    # produces an overlapping band along the spine that obscures the very
    # surface the figure exists to show — the shade pattern already reads the
    # canopy, so the outlines were redundant as well as noisy.
    ax.scatter(trees["x"], trees["y"], s=7, color="white", alpha=0.85,
               linewidths=0, zorder=3, label="Tree (131)")

    ax.add_patch(Rectangle(
        (5, C.SPINE["y_centre_m"] - C.SPINE["width_m"] / 2),
        140, C.SPINE["width_m"], facecolor="none",
        edgecolor="white", linewidth=1.4, linestyle=(0, (6, 4)), zorder=4))
    ax.annotate("The Shaded Spine", xy=(75, C.SPINE["y_centre_m"] + 7.5),
                ha="center", va="bottom", color="white",
                fontsize=10, fontweight="semibold", zorder=5)
    ax.legend(loc="lower right", labelcolor="white", framealpha=0)

    ax.set_xlabel("metres (east →)")
    ax.set_ylabel("metres (north ↑)")
    ax.grid(False)
    cb = fig.colorbar(im, ax=ax, fraction=0.030, pad=0.02)
    cb.set_label("Heat index (°C)", fontsize=9)
    cb.outline.set_visible(False)

    return viz.finish(
        fig, "fig04_site_comfort_map",
        source=f"{SPA}; {NCM}",
        note="Lighter is cooler. The spine reads as the coolest continuous "
             "route across the site; the biodiversity strip is the second "
             "cool pocket. White dots mark the 131 tree positions.",
    )


def fig_model_performance(m1: dict, grid: pd.DataFrame):
    """Predicted versus measured, and the residuals. The honesty check.

    Uses the exact held-out test set the model was scored on, handed over by
    `train_shade_surrogate`. Re-splitting here would draw a different partition
    whose points overlap the training set — which would make the one figure
    whose job is to verify the model the least trustworthy thing in the set.
    """
    X_te, y_te = m1["_test"]
    pred = m1["estimators"]["neural_network"].predict(X_te)

    fig, (ax1, ax2) = viz.open_figure(
        "Does the surrogate actually reproduce the simulation?",
        "Neural network predictions against ray-traced ground truth, held-out test set",
        ncols=2, width=11.0, height=4.8,
    )
    ax1.scatter(y_te, pred, s=9, alpha=0.35, color=C.SERIES[0], edgecolors="none")
    lim = [min(y_te.min(), pred.min()), max(y_te.max(), pred.max())]
    ax1.plot(lim, lim, color=C.PALETTE["muted"], linestyle="--", linewidth=1.2)
    ax1.set_xlabel("Ray-traced shade hours (ground truth)")
    ax1.set_ylabel("Predicted shade hours")
    ax1.set_title(f"R² = {m1['models']['neural_network']['test_r2']:.4f}", fontsize=10)

    resid = pred - y_te
    ax2.scatter(pred, resid, s=9, alpha=0.35, color=C.SERIES[1], edgecolors="none")
    ax2.axhline(0, color=C.PALETTE["muted"], linestyle="--", linewidth=1.2)
    ax2.set_xlabel("Predicted shade hours")
    ax2.set_ylabel("Residual (predicted − actual)")
    ax2.set_title(f"RMSE = {m1['models']['neural_network']['test_rmse']:.1f} hours", fontsize=10)

    return viz.finish(
        fig, "fig05_surrogate_performance",
        source=MODEL,
        note="Residuals scattered evenly about zero indicate no systematic bias.",
    )


def fig_feature_importance(m1: dict):
    """Which design levers move the outcome — the link from model to decision."""
    imp = pd.DataFrame(m1["permutation_importance"]).head(8).iloc[::-1]
    labels = {
        "trees_within_20m": "Trees within 20 m",
        "trees_within_10m": "Trees within 10 m",
        "dist_to_tree_m": "Distance to nearest tree",
        "y": "North–south position",
        "x": "East–west position",
        "dist_to_edge_m": "Distance to site edge",
        "dist_to_spine_m": "Distance to the spine",
        "under_spine_canopy": "Under the spine canopy",
        "canopy_overhead": "Canopy directly overhead",
        "sky_view_factor": "Sky view factor",
        "albedo": "Surface albedo",
    }
    fig, ax = viz.open_figure(
        "What actually determines whether a square metre is shaded",
        "Permutation importance — the drop in accuracy when each feature is shuffled",
        height=4.8,
    )
    bars = ax.barh([labels.get(f, f) for f in imp["feature"]],
                   imp["importance"], xerr=imp["std"],
                   color=C.SERIES[0], error_kw={"ecolor": C.PALETTE["baseline"], "lw": 1})
    viz.bar_gap_style(bars)
    ax.set_xlabel("Importance (drop in R² when shuffled)")
    ax.grid(axis="y", visible=False)

    return viz.finish(
        fig, "fig06_feature_importance",
        source=MODEL,
        note="Tree density within 20 m dominates: the design lever that matters "
             "most is planting density, not canopy width.",
    )


def fig_confusion(m2: dict):
    """Where the comfort classifier gets it wrong."""
    labels = m2["labels"]
    cm = np.array(m2["confusion_matrix"], dtype=float)
    cmn = cm / cm.sum(axis=1, keepdims=True) * 100

    fig, ax = viz.open_figure(
        "Predicting thermal stress from the clock and the sun alone",
        f"Temperature and humidity withheld · test accuracy {m2['test_accuracy']:.1%}",
        width=7.6, height=5.6,
    )
    im = ax.imshow(cmn, cmap=viz.HEAT_CMAP, vmin=0, vmax=100)
    ax.set_xticks(range(len(labels)), labels, rotation=20, ha="right")
    ax.set_yticks(range(len(labels)), labels)
    ax.set_xlabel("Predicted band")
    ax.set_ylabel("Actual band")
    ax.grid(False)
    for i in range(len(labels)):
        for j in range(len(labels)):
            ax.text(j, i, f"{cmn[i, j]:.0f}%", ha="center", va="center",
                    fontsize=9, fontweight="semibold",
                    color="white" if cmn[i, j] > 45 else C.PALETTE["ink"])
    cb = fig.colorbar(im, ax=ax, fraction=0.040, pad=0.03)
    cb.set_label("% of actual band", fontsize=9)
    cb.outline.set_visible(False)

    return viz.finish(
        fig, "fig07_confusion_matrix",
        source=MODEL,
        note="Rows sum to 100%. Errors fall almost entirely between adjacent "
             "bands, never between comfortable and dangerous.",
    )


def fig_microclimate_regimes(m3: dict, hourly: pd.DataFrame):
    """The programming calendar, learned rather than assumed."""
    s = pd.DataFrame(m3["regime_summary"]).sort_values("mean_heat_index_c")
    fig, (ax1, ax2) = viz.open_figure(
        f"The park's {m3['best_k']} operating regimes, found by clustering",
        "k selected by silhouette score, not chosen — daylight hours only",
        ncols=2, width=11.0, height=4.8,
    )

    order = s["regime"].tolist()
    colors = [C.SERIES[i % len(C.SERIES)] for i in range(len(order))]
    bars = ax1.bar([f"R{int(r)}" for r in order], s["hours"], color=colors)
    viz.bar_gap_style(bars)
    ax1.set_ylabel("Daylight hours per year")
    ax1.set_xlabel("Regime (coolest → hottest)")
    for i, (h, hi) in enumerate(zip(s["hours"], s["mean_heat_index_c"])):
        ax1.text(i, h + max(s["hours"]) * 0.02, f"{int(h)} h",
                 ha="center", fontsize=8, color=C.PALETTE["ink_secondary"])

    k = m3["k_selection"]
    ax2.plot([d["k"] for d in k], [d["silhouette"] for d in k],
             marker="o", color=C.SERIES[0])
    ax2.axvline(m3["best_k"], color=C.SERIES[1], linestyle="--", linewidth=1.4)
    ax2.annotate(f"k = {m3['best_k']} selected", xy=(m3["best_k"], max(d["silhouette"] for d in k)),
                 xytext=(0.5, -0.5), textcoords="offset fontsize",
                 fontsize=9, color=C.SERIES[1], fontweight="semibold")
    ax2.set_xlabel("Number of clusters (k)")
    ax2.set_ylabel("Silhouette score")

    return viz.finish(
        fig, "fig08_microclimate_regimes",
        source=MODEL,
        note="Each regime becomes a programming slot in the activation strategy.",
    )


def fig_diurnal_heatmap(hourly: pd.DataFrame):
    """Hour-by-month comfort surface — when the park is usable."""
    fig, (ax1, ax2) = viz.open_figure(
        "When is the park comfortable?",
        "Mean heat index by hour and month — exposed today, shaded as designed",
        ncols=2, width=11.5, height=5.0, sharey=True,
    )
    for ax, col, title in (
        (ax1, "heat_index_c", "Exposed (today)"),
        (ax2, "heat_index_shaded_c", "Under the Shaded Spine"),
    ):
        piv = hourly.pivot_table(index="hour", columns="month", values=col, aggfunc="mean")
        im = ax.imshow(piv.to_numpy(), origin="lower", cmap=viz.HEAT_CMAP,
                       aspect="auto", vmin=15, vmax=55,
                       extent=(0.5, 12.5, -0.5, 23.5))
        ax.set_title(title, fontsize=10)
        ax.set_xticks(range(1, 13), ["J", "F", "M", "A", "M", "J",
                                     "J", "A", "S", "O", "N", "D"])
        ax.set_yticks([0, 6, 12, 18, 23], ["00", "06", "12", "18", "23"])
        ax.set_xlabel("Month")
        ax.grid(False)
    ax1.set_ylabel("Hour of day")
    cb = fig.colorbar(im, ax=[ax1, ax2], fraction=0.030, pad=0.02)
    cb.set_label("Heat index (°C)", fontsize=9)
    cb.outline.set_visible(False)

    return viz.finish(
        fig, "fig09_diurnal_comfort",
        source=f"{NCM} — hourly series MODELLED, see src/climate.py",
        note="The design opens up the late afternoon in spring and autumn, "
             "which is when the catchment most wants to use the park.",
    )


def fig_site_plan(grid: pd.DataFrame, trees: pd.DataFrame):
    """The masterplan, drawn from the same geometry the analysis used."""
    zones = pd.read_csv(C.DATA_RAW / "site_zoning_schedule.csv")

    # Fourteen zones across eight categories is more than any categorical palette
    # can carry — the validated ramp holds six, and a seventh hue is never
    # generated. So this plan does what an architectural drawing does: it names
    # the rooms on the drawing. Fill is a single neutral, and identity comes from
    # the label, not from colour. The spine is the one element given a colour,
    # because it is the one element the whole scheme is about.
    short = {
        "Perimeter Shade Buffer (S)": "Shade buffer (S)",
        "Perimeter Shade Buffer (N)": "Shade buffer (N)",
        "Outdoor Fitness & Wellness": "Fitness",
        "Native Planting / Biodiversity Strip": "Biodiversity\nstrip",
        "Quiet Contemplation Garden": "Quiet\ngarden",
        "Commercial & Service Kiosk Cluster": "Kiosks",
        "Multipurpose Sports Lawn": "Sports lawn",
        "Main Entrance Plaza": "Entry\nW",
        "Secondary Entrance (E)": "Entry\nE",
        "Children's Play Zone": "Children's play",
        "Family Picnic & Shaded Seating": "Family picnic",
        "Community Plaza & Event Lawn": "Community plaza",
    }
    fig, ax = viz.open_figure(
        "Masterplan — zones, planting and the spine",
        "Drawn from site_zoning_schedule.csv, the same geometry the models use",
        width=11.0, height=6.6,
    )
    for _, z in zones.iterrows():
        if z["Zone"].startswith("Path Network"):
            continue
        w, h = z["X_max"] - z["X_min"], z["Y_max"] - z["Y_min"]
        ax.add_patch(Rectangle(
            (z["X_min"], z["Y_min"]), w, h,
            facecolor=C.PALETTE["rule"], alpha=0.55,
            edgecolor=C.PALETTE["baseline"], linewidth=1.0))
        if w * h > 400:
            ax.annotate(
                short.get(z["Zone"], z["Zone"]),
                xy=(z["X_min"] + w / 2, z["Y_min"] + h / 2),
                ha="center", va="center", fontsize=8,
                color=C.PALETTE["ink_secondary"], linespacing=1.25)

    ax.add_patch(Rectangle(
        (5, C.SPINE["y_centre_m"] - C.SPINE["width_m"] / 2), 140, C.SPINE["width_m"],
        facecolor=C.SERIES[0], alpha=0.75, edgecolor=C.SERIES[0], linewidth=1.5,
        zorder=3, label="The Shaded Spine"))
    ax.scatter(trees["x"], trees["y"], s=11, color=C.SERIES[5],
               linewidths=0, zorder=4, label=f"Tree ({len(trees)})")

    ax.set_xlim(-4, C.SITE["length_m"] + 4)
    ax.set_ylim(-4, C.SITE["width_m"] + 4)
    ax.set_aspect("equal")
    ax.set_xlabel("metres (east →)")
    ax.set_ylabel("metres (north ↑)")
    ax.grid(False)
    ax.legend(loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.20))

    return viz.finish(
        fig, "fig10_masterplan",
        source="Phase 5 masterplan geometry; 131 trees from the Phase 6 schedule",
        note=f"Site boundary is an ASSUMED {C.SITE['length_m']:.0f}×"
             f"{C.SITE['width_m']:.0f} m rectangle pending DWG confirmation.",
    )


def build_all(hourly, grid, trees, m1, m2, m3, normals) -> list:
    """Generate the full figure set."""
    viz.apply_style()
    made = [
        fig_climate_profile(normals, hourly),
        fig_comfort_bands(hourly),
        fig_shade_performance(grid, hourly),
        fig_site_comfort_map(grid, trees),
        fig_model_performance(m1, grid),
        fig_feature_importance(m1),
        fig_confusion(m2),
        fig_microclimate_regimes(m3, hourly),
        fig_diurnal_heatmap(hourly),
        fig_site_plan(grid, trees),
    ]
    return made
