"""Randomized optimization for neural network weights: the train/test gap.

PROVENANCE
    assets/pdf/CS7641_ML_Randomized_Optimization_Su24.pdf
    "CS7641 ML Randomized Optimization", Summer 2024, Abanoub Abdelmalak.
    Table IV "Experiments Summary Results", the `mean` row, across 272 runs.
    Task SP-NN: neural network weight optimization for JPM stock buy/sell signal
    prediction, 2009-2021 (train 2159 / test 926 / 18 features, Table I).

    All eight values are the mean row of Table IV, transcribed to six decimals
    and displayed to three.

TAKEAWAY
    This is a negative result and the report says so: optimizing network weights
    with randomized search does not generalize. Every metric loses roughly a
    third to a half of its value from train to test.
"""

import matplotlib.pyplot as plt
import numpy as np

from _style import PALETTE, INK, INK_MUTED, use_style, recessive_grid, save

# Table IV, `mean` row (272 runs)
METRICS = ["Accuracy", "Precision", "Recall", "F1"]
TRAIN = [0.471409, 0.342452, 0.471409, 0.356185]
TEST = [0.293855, 0.257507, 0.293855, 0.210000]

use_style()

x = np.arange(len(METRICS))
w = 0.36

fig, ax = plt.subplots(figsize=(5.2, 2.9))
recessive_grid(ax, axis="y")

ax.bar(x - w / 2, TRAIN, width=w, color=PALETTE[0], label="Train (mean)", zorder=3)
ax.bar(x + w / 2, TEST, width=w, color=PALETTE[1], label="Test (mean)", zorder=3)

for xi, v in zip(x - w / 2, TRAIN):
    ax.text(xi, v + 0.008, f"{v:.3f}", ha="center", va="bottom", fontsize=7, color=INK_MUTED)
for xi, v in zip(x + w / 2, TEST):
    ax.text(xi, v + 0.008, f"{v:.3f}", ha="center", va="bottom", fontsize=7, color=INK)

# annotate the drop, which is the point of the figure
for xi, tr, te in zip(x, TRAIN, TEST):
    drop = (tr - te) / tr * 100
    ax.text(xi, -0.055, f"-{drop:.0f}%", ha="center", va="top", fontsize=7, color=PALETTE[1])

ax.set_xticks(x)
ax.set_xticklabels(METRICS)
ax.set_ylim(0, 0.62)
ax.set_ylabel("Score")
ax.set_title(
    "Randomized search on network weights does not generalize",
    fontsize=9,
    color=INK,
    loc="left",
    pad=20,
)
ax.legend(loc="lower left", bbox_to_anchor=(0, 1.005), ncol=2, fontsize=8, columnspacing=1.4)

save(fig, "ro_nn_generalization_gap")
