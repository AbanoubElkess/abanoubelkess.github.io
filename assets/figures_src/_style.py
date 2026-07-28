"""Shared style and save helper for every figure on this site.

Rules this module enforces, so individual scripts cannot drift:

* Light-mode only. The site sets ``enable_darkmode: false`` in ``_config.yml``,
  so figures are read on a white page.
* Categorical colours come from ``PALETTE`` below, assigned in fixed order and
  never cycled. The order was checked with the dataviz skill's
  ``validate_palette.js``; see README.md for the recorded output.
* SVG output with the embedded date suppressed, so re-running a script
  reproduces its committed file byte for byte. That is what makes "every
  figure regenerates from its source" a checkable claim rather than a promise.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

STYLE = Path(r"C:/Users/aabdelmalak3/.claude/knowledge/photonica.mplstyle")

# Okabe-Ito, ordered so that adjacent pairs keep the largest colour-vision
# separation. Take colours from the front of this list; do not reorder per
# figure, because colour must follow the entity rather than its rank.
PALETTE = ["#0072B2", "#D55E00", "#009E73", "#E69F00"]

INK = "#1a1a1a"
INK_MUTED = "#666666"
GRID = "#e0e0e0"

OUT_DIR = Path(__file__).resolve().parents[1] / "img" / "figures"


def use_style():
    """Apply the house style plus the light-surface tweaks this site needs."""
    if STYLE.exists():
        plt.style.use(str(STYLE))
    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
            "text.color": INK,
            "axes.labelcolor": INK,
            "axes.edgecolor": INK_MUTED,
            "xtick.color": INK_MUTED,
            "ytick.color": INK_MUTED,
            "svg.fonttype": "none",  # keep text as text, not paths
            # without a fixed salt matplotlib randomizes SVG element ids per run,
            # so identical input would still produce a different file
            "svg.hashsalt": "abanoubelkess-figures",
        }
    )


def recessive_grid(ax, axis="y"):
    """Grid lines sit behind the data and never compete with it."""
    ax.grid(axis=axis, color=GRID, linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)


def save(fig, name):
    """Write ``name``.svg into assets/img/figures/, reproducibly."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"{name}.svg"
    # metadata Date=None strips the timestamp matplotlib would otherwise embed
    fig.savefig(path, format="svg", bbox_inches="tight", metadata={"Date": None})
    plt.close(fig)
    print(f"wrote {path}")
