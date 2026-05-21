---
layout: page
title: DRC & Layout Verification Automation
description: AI agentic flows and geometric engines to automate complex EDA physical verification and PDK validation.
importance: 2
category: work
img: /assets/img/eda_agents_thumb.png
---

### Project Overview

Semiconductor physical verification—comprising Design Rule Checking (DRC) and Layout vs. Schematic (LVS)—is the final gatekeeping step before tape-out. At advanced nodes ($7\text{ nm}$ and below), the Process Design Kit (PDK) verification deck contains tens of thousands of complex geometric and electrical rules. Designing layouts that comply with these rules requires a highly repetitive cycle of running verification, analyzing massive error logs, and manually correcting polygon coordinates in GDSII/OASIS layout files.

This project developed an intelligent agentic framework that compiles rule decks, executes verification runs (e.g., using Siemens Calibre), parses violation logs, and executes closed-loop geometric modifications to automatically correct layout DRC violations.

---

### Geometric Layout Operations & Formulation

DRC rules are defined as topological and spatial relations between layout polygons. Our engine models these checks as set-theoretic and distance queries on 2D planar geometries.

#### 1. Minimum Spacing Verification

A minimum spacing rule between metal polygons on a layer $A$ specifies that no two edge segments can lie within a distance $d_{\text{min}}$ of each other:

$$\text{Spacing}(A) = \left\{ (p_1, p_2) \in \partial A \times \partial A \mid \|p_1 - p_2\|_2 < d_{\text{min}} \right\}$$

where $\partial A$ represents the boundary curves of all polygons on layer $A$, and $\|\cdot\|_2$ is the Euclidean norm. If $\text{Spacing}(A) \neq \emptyset$, the coordinates are flagged as a violation.

#### 2. Enclosure and Extension Verification

For overlapping layers (e.g., contact vias $A$ and metal routes $B$), the metal layer must enclose the via by a minimum extension distance $e_{\text{min}}$:

$$\text{Enclosure}(A, B) = \left\{ p \in \partial A \mid \min_{q \in \partial B} \|p - q\|_2 < e_{\text{min}} \right\}$$

Our engine compiles these constraints into a computational DAG (Directed Acyclic Graph) of Boolean operations (AND, OR, NOT, XOR), sizing (dilation/erosion), and distance searches.

---

### Hierarchical Layout Processing & Agentic Flow

To handle modern layout files containing billions of transistors, flat processing is infeasible. The engine processes layouts hierarchically using a cell dependency graph:

$$H = (C, E)$$

where:

- $C$ represents the set of cells (sub-circuits and standard cells).
- $E$ represents instantiation edges representing parent-child relationships in the layout tree.

The automated verification and repair system is orchestrated as a collaborative multi-agent workflow:

```
        Raw Layout (GDSII/OASIS)
                    │
                    ▼
       ┌─────────────────────────┐
       │   DRC Engine (Calibre)  │
       └─────────────────────────┘
                    │
                    ▼
          DRC Violation Database
                    │
                    ▼
       ┌─────────────────────────┐
       │     Log Parser Agent    │ ──► Extracts coordinate & rule violations
       └─────────────────────────┘
                    │
                    ▼
       ┌─────────────────────────┐
       │  Geometry Analyzer Agent│ ──► Crops local cell hierarchy bounding box
       └─────────────────────────┘
                    │
                    ▼
       ┌─────────────────────────┐
       │  Auto-Corrector Agent   │ ──► Computes layout shift/sizing updates
       └─────────────────────────┘
                    │
                    ▼
          Updated GDSII / OASIS
```

1. **Log Parser Agent**: Ingests massive ascii/binary DRC summary reports and classifies error signatures.
2. **Geometry Analyzer Agent**: Identifies the local cell coordinate boundaries and extracts the local polygon mesh surrounding the violation.
3. **Auto-Corrector Agent**: Formulates a localized constrained optimization problem:

   $$\min_{\Delta x, \Delta y} \sum_{i} \left( \Delta x_i^2 + \Delta y_i^2 \right)$$

   subject to meeting the DRC minimum spacing/width constraints and preserving electrical connectivity (no LVS shorts/opens).

---

### Key Outcomes & Technical Impact

- **Automated Repair**: Automatically resolved **$82\%$** of typical post-routing DRC violations (width, spacing, and enclosure errors) across sub-blocks, eliminating manual layout modifications.
- **Coverage & Scaling**: Enabled parallel verification runs on heterogeneous compute clusters, leading to a **$25\%$** improvement in rule coverage validation for complex custom layouts.
- **Cycle Time Reduction**: Decreased standard physical verification iterations from days to under 3 hours, facilitating rapid design-technology co-optimization (DTCO) workflows.
