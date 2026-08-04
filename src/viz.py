"""
The visual system for every figure in the Al Safa 2 Park submission.

Why this module exists
----------------------
The earlier version of this project produced charts from a dozen unrelated
scripts. Each picked its own colours, fonts, figure size and title style, so the
submission read as a folder of unrelated images rather than one document. Worse,
three of the five headline charts used a twin y-axis (`ax.twinx()`), which lets
the author slide two unrelated scales against each other until the lines appear
to correlate. It is the single most criticised mistake in statistical graphics.

Every figure in the submission is now built through `open_figure()` and closed
through `finish()`. That guarantees, by construction:

  * one palette, validated for colour-vision deficiency (see config.py)
  * one typeface, one figure width, one title treatment
  * a source line on every single figure, so a juror can trace any number
  * no dual y-axes anywhere — `stacked_panels()` is the honest replacement

Usage
-----
    from src import viz
    fig, ax = viz.open_figure("Monthly heat index", "Exposed vs shaded")
    ax.plot(...)
    viz.finish(fig, "fig_03_heat_index", source="NCM normals 1977-2015")
"""

from __future__ import annotations

from typing import Iterable, Sequence

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from . import config as C

# Registered once so every heat surface in the project uses the same ramp.
HEAT_CMAP = LinearSegmentedColormap.from_list("alsafa_heat", C.HEAT_RAMP, N=256)


def apply_style() -> None:
    """Install the project's matplotlib defaults. Call once per session."""
    mpl.rcParams.update({
        "figure.facecolor": C.PALETTE["paper"],
        "axes.facecolor": C.PALETTE["paper"],
        "savefig.facecolor": C.PALETTE["paper"],
        "savefig.dpi": C.FIGURE["dpi"],
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.30,

        "font.family": "sans-serif",
        "font.sans-serif": [C.FIGURE["font_family"], "Segoe UI", "Arial"],
        "font.size": C.FIGURE["label_size"],

        "text.color": C.PALETTE["ink"],
        "axes.labelcolor": C.PALETTE["ink_secondary"],
        "axes.labelsize": C.FIGURE["label_size"],
        "axes.titlesize": C.FIGURE["title_size"],
        "axes.titleweight": "semibold",
        "axes.titlecolor": C.PALETTE["ink"],
        "axes.titlelocation": "left",
        "axes.titlepad": 10,

        # Recessive chrome: the data should be the only assertive thing here.
        "axes.edgecolor": C.PALETTE["baseline"],
        "axes.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.color": C.PALETTE["rule"],
        "grid.linewidth": 0.7,
        "grid.alpha": 1.0,

        "xtick.color": C.PALETTE["muted"],
        "ytick.color": C.PALETTE["muted"],
        "xtick.labelsize": C.FIGURE["tick_size"],
        "ytick.labelsize": C.FIGURE["tick_size"],
        "xtick.direction": "out",
        "ytick.direction": "out",
        "xtick.major.size": 0,
        "ytick.major.size": 0,

        "legend.frameon": False,
        "legend.fontsize": C.FIGURE["label_size"] - 1,
        "legend.labelcolor": C.PALETTE["ink_secondary"],

        "lines.linewidth": 2.0,          # 2px lines, per the mark spec
        "lines.markersize": 5.0,
        "lines.solid_capstyle": "round",

        "axes.prop_cycle": mpl.cycler(color=C.SERIES),
    })


def open_figure(
    title: str,
    subtitle: str | None = None,
    *,
    width: float | None = None,
    height: float | None = None,
    nrows: int = 1,
    ncols: int = 1,
    **kwargs,
):
    """Open a figure carrying the project's standard title treatment.

    Returns ``(fig, ax)`` for a single panel, or ``(fig, axes)`` for a grid.
    """
    fig, ax = plt.subplots(
        nrows,
        ncols,
        figsize=(width or C.FIGURE["width_in"], height or C.FIGURE["height_in"]),
        **kwargs,
    )
    fig.suptitle(
        title,
        x=0.012,
        y=0.995,
        ha="left",
        va="top",
        fontsize=C.FIGURE["title_size"],
        fontweight="semibold",
        color=C.PALETTE["ink"],
    )
    if subtitle:
        fig.text(
            0.012,
            0.945,
            subtitle,
            ha="left",
            va="top",
            fontsize=C.FIGURE["label_size"],
            color=C.PALETTE["ink_secondary"],
        )
    return fig, ax


def stacked_panels(
    title: str,
    subtitle: str | None = None,
    *,
    ratios: Sequence[float] = (1, 1),
    height: float | None = None,
):
    """Two measures of different scale, drawn honestly.

    This is the replacement for `ax.twinx()`. Sharing an x-axis across stacked
    panels lets the reader compare timing without implying that two unrelated
    y-scales are commensurate. A dual-axis chart can be made to show almost any
    relationship by choosing the two scales; this cannot.
    """
    n = len(ratios)
    fig, axes = plt.subplots(
        n,
        1,
        figsize=(C.FIGURE["width_in"], height or (C.FIGURE["height_in"] * 1.15)),
        sharex=True,
        gridspec_kw={"height_ratios": list(ratios), "hspace": 0.18},
    )
    fig.suptitle(
        title, x=0.012, y=0.995, ha="left", va="top",
        fontsize=C.FIGURE["title_size"], fontweight="semibold",
        color=C.PALETTE["ink"],
    )
    if subtitle:
        fig.text(
            0.012, 0.955, subtitle, ha="left", va="top",
            fontsize=C.FIGURE["label_size"], color=C.PALETTE["ink_secondary"],
        )
    return fig, axes


def finish(fig, name: str, *, source: str, note: str | None = None,
           save: bool = True, save_to=None):
    """Add the mandatory source strip and write the figure out.

    `source` is not optional. A figure whose provenance cannot be stated in one
    line has no business in the submission.

    `save_to` overrides the destination directory. Charts go to figures/; the
    technical drawings in `src.drawings` go to design/visuals/, but they are
    held to the same rule about carrying their source.
    """
    strip = f"Source: {source}   ·   {C.PROJECT_STAMP}"
    if note:
        strip = f"{note}\n{strip}"
    fig.text(
        0.012,
        0.005,
        strip,
        ha="left",
        va="bottom",
        fontsize=C.FIGURE["caption_size"],
        color=C.PALETTE["muted"],
        linespacing=1.35,
    )
    lines = strip.count("\n") + 1
    bottom = max(0.045, 0.018 * lines + 0.025)
    fig.tight_layout(rect=(0, bottom, 1, 0.93))
    if save:
        out = (save_to or C.FIGURES) / f"{name}.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out)
        plt.close(fig)
        return out
    return None


def label_last(ax, x, y, text: str, color: str, *, dx: float = 0.4, dy: float = 0.0):
    """Direct-label a series at its final point, so the legend is a backstop."""
    ax.annotate(
        text,
        xy=(x, y),
        xytext=(dx, dy),
        textcoords="offset fontsize",
        va="center",
        fontsize=C.FIGURE["label_size"] - 1,
        fontweight="semibold",
        color=color,
    )


def comfort_legend(ax, *, loc: str = "upper left", ncol: int = 4):
    """Legend for the four comfort bands, always with visible text labels.

    Status colour never carries the meaning on its own — that is the rule these
    four colours are reserved under.
    """
    from matplotlib.patches import Patch

    handles = [
        Patch(facecolor=C.COMFORT_COLORS[b], label=b, edgecolor="none")
        for b in C.COMFORT_ORDER
    ]
    ax.legend(handles=handles, loc=loc, ncol=ncol, handlelength=1.1, columnspacing=1.4)


def shade_comfort_bands(ax, *, alpha: float = 0.10):
    """Wash the comfort thresholds across a temperature axis as a reading aid."""
    for name, lo, hi in C.COMFORT_BANDS:
        ax.axhspan(
            max(lo, ax.get_ylim()[0]),
            min(hi, ax.get_ylim()[1]),
            color=C.COMFORT_COLORS[name],
            alpha=alpha,
            zorder=0,
            linewidth=0,
        )


def bar_gap_style(bars: Iterable, *, surface: str | None = None):
    """Apply the 2px surface gap between adjacent/stacked fills."""
    surface = surface or C.PALETTE["paper"]
    for b in bars:
        b.set_edgecolor(surface)
        b.set_linewidth(2.0)
