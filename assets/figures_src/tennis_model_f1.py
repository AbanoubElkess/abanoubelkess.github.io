"""Tennis match winner prediction: train vs test F1 across the five models tried.

PROVENANCE
    assets/pdf/TennisMatchPrediction_Project.pdf
    "Tennis Match Winner Predictions", CSE6242 Data & Visual Analytics, Fall 2022.
    Abanoub Abdelmalak, Sheikh Jalaluddin Mohammad, Michael S Rivera, Mohamad A Elsayed.
    Section 5.4 "Final Machine Learning Model Review", the Train/Test F1 table on page 4.

    Every number below is transcribed from that table. Nothing is interpolated,
    rounded up, or added.

TAKEAWAY
    Gradient boosting gives the best generalization (test F1 0.733). AdaBoost
    reaches a perfect training F1 of 1.000 and still lands slightly below it on
    test, which is memorization rather than skill.
"""

import matplotlib.pyplot as plt
import numpy as np

from _style import PALETTE, INK, INK_MUTED, use_style, recessive_grid, save

# (model, train F1, test F1) exactly as printed in the report table
RESULTS = [
    ("Decision Tree", 0.712383, 0.676517),
    ("Gradient Boosting", 0.812047, 0.733461),
    ("Neural Network", 0.712053, 0.705958),
    ("Ada Boost", 1.000000, 0.730786),
    ("K Nearest Neighbors", 0.719273, 0.684189),
]

use_style()

# sort by test F1 so the ranking the reader cares about is the vertical order
rows = sorted(RESULTS, key=lambda r: r[2])
labels = [r[0] for r in rows]
train = np.array([r[1] for r in rows])
test = np.array([r[2] for r in rows])

y = np.arange(len(rows))
h = 0.36

fig, ax = plt.subplots(figsize=(5.6, 3.1))

recessive_grid(ax, axis="x")

ax.barh(y + h / 2, train, height=h, color=PALETTE[0], label="Train F1", zorder=3)
ax.barh(y - h / 2, test, height=h, color=PALETTE[1], label="Test F1", zorder=3)

# direct labels: the contrast check obliges visible values rather than colour alone
for yi, v in zip(y + h / 2, train):
    ax.text(v + 0.012, yi, f"{v:.3f}", va="center", ha="left", fontsize=7, color=INK_MUTED)
for yi, v in zip(y - h / 2, test):
    ax.text(v + 0.012, yi, f"{v:.3f}", va="center", ha="left", fontsize=7, color=INK)

ax.set_yticks(y)
ax.set_yticklabels(labels)
ax.set_xlim(0, 1.16)
ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_xlabel("F1 score")
ax.set_title(
    "Gradient boosting generalizes best; AdaBoost only memorizes",
    fontsize=9,
    color=INK,
    loc="left",
    pad=22,
)
# legend above the plot so it can never sit on top of a bar or its label
ax.legend(
    loc="lower left",
    bbox_to_anchor=(0, 1.005),
    ncol=2,
    fontsize=8,
    columnspacing=1.4,
)
ax.spines["left"].set_visible(False)
ax.tick_params(axis="y", length=0)

save(fig, "tennis_model_f1")
