"""Research positioning diagram for the About page.

WHAT THIS ASSERTS
    Three fields Abanoub works across, the pairwise areas they create, and the
    PhD objective at their confluence. Unlike the other figures here this one
    plots no measurements; every label is a claim about the work, sourced from
    the site's own text:

      "Machine Learning"           MSc CS (ML specialization), Georgia Tech
      "Quantum Computing"          PhD focus, Adibi group (_pages/about.md)
      "Semiconductor & EDA"        Siemens Digital Industries Software, RET/OPC
      "AI for EDA"                 SVRF Copilot on LangChain/MCP (about.md);
                                   ICLAD 2025 paper (_bibliography/papers.bib)
      "ML-based quantum error
       correction"                 stated PhD research focus (about.md)
      "Quantum hardware design"    the quantum/semiconductor overlap
      centre: "Quantum Machine
       Learning"                   the PhD objective, confirmed by Abanoub

    Nothing here is a result. If any label stops being true, edit it here and
    re-run rather than editing the SVG.

LAYOUT
    Three equal circles with centres on a ring of radius 0.55 and radius 1.0, so
    all three pairwise lenses and the central triple region are large enough to
    label. Leader lines point at a dot inside the region they name, so no label
    has to sit inside a cramped lens.
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch

from _style import INK, INK_MUTED, use_style, save

# circle hue per field, taken from the validated categorical palette
FIELDS = [
    # (label, angle of centre in degrees, colour)
    ("Quantum Computing", 90, "#0072B2"),
    ("Machine Learning", 210, "#D55E00"),
    ("Semiconductor & EDA", 330, "#009E73"),
]
R = 1.0
D = 0.55
ALPHA = 0.42

use_style()
fig, ax = plt.subplots(figsize=(7.4, 6.0))
ax.set_aspect("equal")
ax.axis("off")


def polar(angle_deg, radius):
    a = np.radians(angle_deg)
    return radius * np.cos(a), radius * np.sin(a)


centres = {}
for label, angle, colour in FIELDS:
    cx, cy = polar(angle, D)
    centres[label] = (cx, cy)
    ax.add_patch(Circle((cx, cy), R, facecolor=colour, edgecolor="none", alpha=ALPHA, zorder=2))

# --- field names and icons, kept clear of each other inside each lobe ------
# (display text, name xy, icon xy). Explicit cartesian, because the name and the
# icon have to sit at different depths in the lobe or they overlap.
# Icon anchors are pulled in far enough that the icon's widest reach stays inside
# the circle. Checked arithmetically: centre-to-anchor distance plus the icon's
# reach must stay below R, and the chip icon (pins at 0.82 * scale) is the widest.
LOBES = {
    "Quantum Computing": ("Quantum Computing", (0.0, 0.92), (0.0, 1.24)),
    "Machine Learning": ("Machine\nLearning", (-1.00, -0.20), (-0.92, -0.62)),
    "Semiconductor & EDA": ("Semiconductor\n& EDA", (1.00, -0.20), (0.92, -0.62)),
}
for label, _, _ in FIELDS:
    text, (nx, ny), _ = LOBES[label]
    ax.text(
        nx, ny, text, ha="center", va="center", fontsize=10, color=INK,
        fontweight="semibold", linespacing=1.2, zorder=6,
    )


# --- small icons inside each lobe -----------------------------------------
def icon_quantum(x, y, s=0.30):
    """Two qubit wires, a Hadamard box, and a CNOT."""
    for dy in (s * 0.42, -s * 0.42):
        ax.plot([x - s, x + s], [y + dy, y + dy], color=INK, lw=1.1, zorder=6)
    ax.add_patch(
        FancyBboxPatch(
            (x - s * 0.72, y + s * 0.16),
            s * 0.52,
            s * 0.52,
            boxstyle="square,pad=0",
            facecolor="white",
            edgecolor=INK,
            lw=1.1,
            zorder=7,
        )
    )
    ax.text(x - s * 0.46, y + s * 0.42, "H", ha="center", va="center", fontsize=7, color=INK, zorder=8)
    ax.plot([x + s * 0.34], [y + s * 0.42], marker="o", ms=4, color=INK, zorder=7)
    ax.plot([x + s * 0.34, x + s * 0.34], [y + s * 0.42, y - s * 0.42], color=INK, lw=1.1, zorder=6)
    ax.add_patch(Circle((x + s * 0.34, y - s * 0.42), s * 0.18, facecolor="white", edgecolor=INK, lw=1.1, zorder=7))
    ax.plot([x + s * 0.16, x + s * 0.52], [y - s * 0.42, y - s * 0.42], color=INK, lw=1.0, zorder=8)
    ax.plot([x + s * 0.34, x + s * 0.34], [y - s * 0.60, y - s * 0.24], color=INK, lw=1.0, zorder=8)


def icon_network(x, y, s=0.30):
    """A small 3-2 feedforward graph."""
    left = [(x - s * 0.62, y + s * 0.62), (x - s * 0.62, y), (x - s * 0.62, y - s * 0.62)]
    right = [(x + s * 0.62, y + s * 0.34), (x + s * 0.62, y - s * 0.34)]
    for lx, ly in left:
        for rx, ry in right:
            ax.plot([lx, rx], [ly, ry], color=INK, lw=0.8, zorder=6)
    for px, py in left + right:
        ax.add_patch(Circle((px, py), s * 0.16, facecolor="white", edgecolor=INK, lw=1.0, zorder=7))


def icon_chip(x, y, s=0.30):
    """A die outline with pins and a nested layout pattern."""
    ax.add_patch(
        FancyBboxPatch(
            (x - s * 0.60, y - s * 0.60),
            s * 1.2,
            s * 1.2,
            boxstyle="square,pad=0",
            facecolor="white",
            edgecolor=INK,
            lw=1.2,
            zorder=7,
        )
    )
    for i in (-1, 0, 1):
        off = i * s * 0.34
        ax.plot([x - s * 0.82, x - s * 0.60], [y + off, y + off], color=INK, lw=1.0, zorder=6)
        ax.plot([x + s * 0.60, x + s * 0.82], [y + off, y + off], color=INK, lw=1.0, zorder=6)
        ax.plot([x + off, x + off], [y + s * 0.60, y + s * 0.82], color=INK, lw=1.0, zorder=6)
        ax.plot([x + off, x + off], [y - s * 0.82, y - s * 0.60], color=INK, lw=1.0, zorder=6)
    ax.add_patch(
        FancyBboxPatch(
            (x - s * 0.26, y - s * 0.26),
            s * 0.52,
            s * 0.52,
            boxstyle="square,pad=0",
            facecolor="none",
            edgecolor=INK,
            lw=0.9,
            zorder=8,
        )
    )


icon_quantum(*LOBES["Quantum Computing"][2])
icon_network(*LOBES["Machine Learning"][2])
icon_chip(*LOBES["Semiconductor & EDA"][2])

# --- pairwise regions, named on leader lines -------------------------------
# (text, text angle, text radius, dot angle, dot radius, wrapped label)
PAIRS = [
    ("ML-based quantum\nerror correction", 158, 1.78, 150, 0.80),
    ("AI for EDA\nSVRF Copilot, OPC", 252, 1.62, 270, 0.80),
    ("Quantum hardware\ndesign", 22, 1.78, 30, 0.80),
]
for text, ta, tr, da, dr in PAIRS:
    tx, ty = polar(ta, tr)
    dx, dy = polar(da, dr)
    ax.plot([tx, dx], [ty, dy], color=INK, lw=1.0, zorder=5, solid_capstyle="round")
    ax.plot([dx], [dy], marker="o", ms=5, color=INK, zorder=6)
    ha = "right" if np.cos(np.radians(ta)) < -0.2 else ("left" if np.cos(np.radians(ta)) > 0.2 else "center")
    ax.text(tx, ty, text, ha=ha, va="center", fontsize=8.5, color=INK, zorder=6)

# --- the centre: the PhD objective ----------------------------------------
ax.text(
    0,
    0.02,
    "Quantum\nMachine\nLearning",
    ha="center",
    va="center",
    fontsize=8.6,
    color=INK,
    fontweight="bold",
    linespacing=1.3,
    zorder=8,
)

ax.set_xlim(-2.60, 2.60)
ax.set_ylim(-1.95, 1.85)

save(fig, "research_venn")
