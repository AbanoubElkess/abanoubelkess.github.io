"""Randomized optimization: converged mean fitness by algorithm and problem size.

PROVENANCE
    assets/pdf/CS7641_ML_Randomized_Optimization_Su24.pdf
    "CS7641 ML Randomized Optimization", Summer 2024, Abanoub Abdelmalak (sole author).
    Section IV "Results and Discussion", subsections A (RHC), B (SA), C (GA).
    Problems and sizes from Table I: Flip Flop [40, 100, 500], N-Queens [20, 50, 100].
    Implemented with mlrose-hiive.

    HONESTY NOTE: the report reports these converged values in prose rather than
    in a results table, and states several of them as approximations ("stabilizes
    around 120", "climbs to around 2500"). They are transcribed here exactly as
    written, and the caption on the site says they are the report's own stated
    values. No value has been sharpened, smoothed, or invented. Where the report
    gives a range the lower bound is used.

TAKEAWAY
    GA converges to the highest fitness on both problems, and its margin over
    RHC and SA widens sharply with problem size on N-Queens.
"""

import matplotlib.pyplot as plt
import numpy as np

from _style import PALETTE, INK, INK_MUTED, use_style, recessive_grid, save

ALGOS = ["RHC", "SA", "GA"]

# problem -> sizes, and converged mean fitness per algorithm in ALGOS order
PROBLEMS = {
    "Flip Flop": {
        "sizes": [40, 100, 500],
        "RHC": [32.5, 82, 400],
        "SA": [35, 90, 400],
        "GA": [40, 90, 425],
    },
    "N-Queens": {
        "sizes": [20, 50, 100],
        "RHC": [120, 320, 400],
        "SA": [140, 300, 400],
        "GA": [175, 800, 2500],
    },
}

use_style()

fig, axes = plt.subplots(1, 2, figsize=(6.4, 2.9))

for ax, (problem, data) in zip(axes, PROBLEMS.items()):
    sizes = data["sizes"]
    x = np.arange(len(sizes))
    w = 0.26
    recessive_grid(ax, axis="y")

    for i, algo in enumerate(ALGOS):
        offset = (i - 1) * w
        vals = data[algo]
        ax.bar(x + offset, vals, width=w, color=PALETTE[i], label=algo, zorder=3)
        for xi, v in zip(x + offset, vals):
            ax.text(
                xi,
                v,
                f"{v:g}",
                ha="center",
                va="bottom",
                fontsize=6.5,
                color=INK_MUTED,
                rotation=90,
                zorder=4,
            )

    ax.set_xticks(x)
    ax.set_xticklabels([str(s) for s in sizes])
    ax.set_xlabel("Problem size")
    ax.set_title(problem, fontsize=9, color=INK, loc="left")
    ax.set_ylim(0, max(max(data[a]) for a in ALGOS) * 1.35)

axes[0].set_ylabel("Converged mean fitness")
axes[0].legend(loc="upper left", fontsize=8, ncol=1)

fig.suptitle(
    "Genetic algorithms lead on both problems, decisively so on N-Queens",
    fontsize=9,
    color=INK,
    x=0.005,
    ha="left",
    y=1.06,
)

save(fig, "ro_converged_fitness")
