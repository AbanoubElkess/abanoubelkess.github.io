"""Randomized optimization: how much the configuration matters, across 272 runs.

PROVENANCE
    assets/pdf/CS7641_ML_Randomized_Optimization_Su24.pdf
    "CS7641 ML Randomized Optimization", Summer 2024, Abanoub Abdelmalak.
    Table IV "Experiments Summary Results", the min / 25% / 50% / 75% / max rows
    for the test-set columns. Task SP-NN (neural network weight optimization on
    JPM stock signals).

    A box plot encodes exactly a five-number summary, which is exactly what
    Table IV reports, so nothing is estimated to draw this. Whiskers are the
    table's min and max, not a 1.5*IQR rule, and the figure says so.

    accuracy_test and recall_test are identical in the source table across every
    percentile, so they are drawn as a single box rather than two identical ones
    presented as separate findings.

TAKEAWAY
    The configuration dominates the result. Test F1 ranges from 0.022 to 0.653
    depending on hidden layers, activation, population size and cooling schedule,
    with a median of only 0.102.
"""

import matplotlib.pyplot as plt

from _style import PALETTE, INK, INK_MUTED, use_style, recessive_grid, save

# Table IV test columns: (label, min, q1, median, q3, max)
STATS = [
    ("Accuracy\n(= Recall)", 0.111831, 0.226904, 0.226904, 0.463533, 0.685575),
    ("Precision", 0.012506, 0.051486, 0.226904, 0.483845, 0.716241),
    ("F1", 0.022497, 0.083928, 0.101572, 0.455068, 0.653085),
]

use_style()

bxp_stats = [
    {"label": lab, "whislo": lo, "q1": q1, "med": med, "q3": q3, "whishi": hi, "fliers": []}
    for lab, lo, q1, med, q3, hi in STATS
]

fig, ax = plt.subplots(figsize=(5.2, 3.0))
recessive_grid(ax, axis="y")

bp = ax.bxp(
    bxp_stats,
    showfliers=False,
    patch_artist=True,
    widths=0.45,
    zorder=3,
    medianprops={"color": INK, "linewidth": 1.6},
    whiskerprops={"color": INK_MUTED, "linewidth": 1.0},
    capprops={"color": INK_MUTED, "linewidth": 1.0},
    boxprops={"edgecolor": INK_MUTED, "linewidth": 0.8},
)
for patch, colour in zip(bp["boxes"], PALETTE):
    patch.set_facecolor(colour)
    patch.set_alpha(0.35)

# label the extremes, which are the point of the figure
for i, (lab, lo, q1, med, q3, hi) in enumerate(STATS, start=1):
    ax.text(i + 0.28, hi, f"{hi:.3f}", va="center", fontsize=7, color=INK_MUTED)
    ax.text(i + 0.28, lo, f"{lo:.3f}", va="center", fontsize=7, color=INK_MUTED)
    ax.text(i - 0.30, med, f"{med:.3f}", va="center", ha="right", fontsize=7, color=INK)

ax.set_ylim(-0.03, 0.80)
ax.set_ylabel("Test score")
ax.set_xlim(0.4, 3.8)
ax.set_title(
    "Configuration, not method, decides the outcome",
    fontsize=9,
    color=INK,
    loc="left",
    pad=8,
)
ax.text(
    0.0,
    -0.24,
    "Box = quartiles, line = median, whiskers = observed min and max over 272 runs.",
    transform=ax.transAxes,
    fontsize=7,
    color=INK_MUTED,
)

save(fig, "ro_run_spread")
