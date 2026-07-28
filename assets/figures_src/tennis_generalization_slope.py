"""Tennis prediction: which models generalize, as opposed to which score highest.

PROVENANCE
    assets/pdf/TennisMatchPrediction_Project.pdf
    "Tennis Match Winner Predictions", CSE6242 Data & Visual Analytics, Fall 2022.
    Abanoub Abdelmalak, Sheikh Jalaluddin Mohammad, Michael S Rivera, Mohamad A Elsayed.
    Section 5.4, the Train/Test F1 table on page 4. Same five rows as
    tennis_model_f1.py; this figure asks a different question of them.

TAKEAWAY
    AdaBoost has the steepest fall of any model, from a perfect 1.000 on train to
    0.731 on test. The neural network has the flattest line, losing only 0.006,
    even though it never reaches the top score.

DESIGN NOTE
    Five series would exceed the four-colour validated palette, so identity is
    carried by direct labels and only the two models that carry the finding are
    coloured. The rest stay neutral grey. Colour follows the entity, not its rank.
"""

import matplotlib.pyplot as plt

from _style import PALETTE, INK, INK_MUTED, use_style, save

# (model, train F1, test F1) as printed in the report table
RESULTS = [
    ("Ada Boost", 1.000000, 0.730786),
    ("Gradient Boosting", 0.812047, 0.733461),
    ("K Nearest Neighbors", 0.719273, 0.684189),
    ("Decision Tree", 0.712383, 0.676517),
    ("Neural Network", 0.712053, 0.705958),
]

HIGHLIGHT = {"Ada Boost": PALETTE[1], "Gradient Boosting": PALETTE[0]}
NEUTRAL = "#9a9a9a"

def spread(values, gap):
    """Nudge label positions apart so text never overlaps, preserving order.

    Returns a y position per input index. Several models land within a few
    thousandths of each other, which is exactly the finding, so the labels have
    to stay legible without moving the plotted points.
    """
    order = sorted(range(len(values)), key=lambda i: values[i])
    out = list(values)
    for slot, i in enumerate(order):
        if slot == 0:
            continue
        prev = out[order[slot - 1]]
        if out[i] - prev < gap:
            out[i] = prev + gap
    return out


use_style()
fig, ax = plt.subplots(figsize=(5.0, 3.3))

train_lab = spread([r[1] for r in RESULTS], 0.018)
test_lab = spread([r[2] for r in RESULTS], 0.018)

for (name, tr, te), tly, tey in zip(RESULTS, train_lab, test_lab):
    colour = HIGHLIGHT.get(name, NEUTRAL)
    lw = 1.8 if name in HIGHLIGHT else 1.0
    z = 4 if name in HIGHLIGHT else 2
    ax.plot([0, 1], [tr, te], color=colour, linewidth=lw, marker="o", markersize=4, zorder=z)
    ax.text(-0.03, tly, f"{tr:.3f}", ha="right", va="center", fontsize=7, color=colour, zorder=z)
    ax.text(
        1.03,
        tey,
        f"{te:.3f}  {name}",
        ha="left",
        va="center",
        fontsize=7.5,
        color=colour,
        zorder=z,
    )

# the drop each model takes, annotated on the two that matter
for name, tr, te in RESULTS:
    if name in HIGHLIGHT:
        ax.annotate(
            f"-{tr - te:.3f}",
            xy=(0.5, (tr + te) / 2),
            fontsize=7,
            color=HIGHLIGHT[name],
            ha="center",
            va="bottom",
            zorder=5,
        )

ax.set_xlim(-0.32, 1.62)
ax.set_ylim(0.63, 1.04)
ax.set_xticks([0, 1])
ax.set_xticklabels(["Train F1", "Test F1"])
ax.set_ylabel("F1 score")
ax.spines["bottom"].set_visible(False)
ax.tick_params(axis="x", length=0)
ax.set_title(
    "AdaBoost falls furthest; the neural network barely moves",
    fontsize=9,
    color=INK,
    loc="left",
    pad=8,
)

save(fig, "tennis_generalization_slope")
