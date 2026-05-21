---
layout: page
title: DRC & Layout Verification Automation
description: AI agentic flows and geometric engines to automate complex EDA physical verification and PDK validation.
importance: 2
category: work
area: "Electronic Design Automation (EDA)"
img: /assets/img/eda_agents_thumb.png
toc:
  sidebar: left
---

### Project Overview

Semiconductor physical verification—comprising Design Rule Checking (DRC) and Layout vs. Schematic (LVS)—is the final gatekeeping step before tape-out. At advanced nodes ($7\text{ nm}$ and below), the Process Design Kit (PDK) verification deck contains tens of thousands of complex geometric and electrical rules. Designing layouts that comply with these rules requires a highly repetitive cycle of running verification, analyzing massive error logs, and manually correcting polygon coordinates in GDSII/OASIS layout files.

This project developed an intelligent agentic framework that compiles rule decks, executes verification runs (e.g., using Siemens Calibre), parses violation logs, and executes closed-loop geometric modifications to automatically correct layout DRC violations.

---

### PDK Verification & Constraint Compilation

Verification decks are written in languages like SVRF or TVF (Tcl Verification Format). The deck compiles into an execution tree of layer operations.

#### 1. Layer Definitions and Derived Layers

Layout files store raw layers (e.g. active area, poly-silicon gate, metal routing). The compiler first derives functional layers using Boolean operations:

$$\text{Gate} = \text{Poly} \cap \text{Active}$$

This gate layer is then used to verify channel length, channel width, and source/drain spacings.

#### 2. DRC Violation Database (DFDB)

When verification runs, the DRC engine writes violations to a Database. The database stores the violating rule name, cell name, and coordinates of the polygon vertices causing the error. Our tool parses this data to build a spatial index of errors.

---

### Geometric Layout Verification Operations

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

### Hierarchical Layout Processing & Cell Trees

To handle modern layout files containing billions of transistors, flat processing is infeasible. The engine processes layouts hierarchically using a cell dependency graph:

$$H = (C, E)$$

where:

- $C$ represents the set of cells (sub-circuits and standard cells).
- $E$ represents instantiation edges representing parent-child relationships in the layout tree.

By traversing $H$ in reverse topological order (bottom-up), our engine corrects violations inside leaf cells first (e.g., standard cells). This ensures that corrections propagate automatically to all parent instances, avoiding duplicate calculations and maintaining hierarchical consistency.

---

### Collaborative Multi-Agent Layout Repair Flow

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

1. **Log Parser Agent**: Ingests massive ascii/binary DRC summary reports, extracts error codes, cell references, and coordinate polygons, and builds a spatial index using an R-tree.
2. **Geometry Analyzer Agent**: Identifies the local cell coordinate boundaries and extracts the local polygon mesh surrounding the violation. It crops the layout to isolate the problem region.
3. **Auto-Corrector Agent**: Formulates a localized constrained optimization problem to resolve spacing or width violations by adjusting polygon vertex positions:

   $$\min_{\Delta \mathbf{x}, \Delta \mathbf{y}} \sum_{i} \left( \Delta x_i^2 + \Delta y_i^2 \right)$$

   subject to:
   - Spacing constraints: $x_{i, \text{right}} - x_{j, \text{left}} \ge d_{\text{min}}$ (for horizontal spacing errors).
   - Electrical connectivity preservation: ensuring no new shorts or opens are created by comparing the modified layout graph against the schematic network (LVS validation).

---

### Key Outcomes & Technical Impact

- **Automated Repair**: Automatically resolved **$82\%$** of typical post-routing DRC violations (width, spacing, and enclosure errors) across sub-blocks, eliminating manual layout modifications.
- **Coverage & Scaling**: Enabled parallel verification runs on heterogeneous compute clusters, leading to a **$25\%$** improvement in rule coverage validation for complex custom layouts.
- **Cycle Time Reduction**: Decreased standard physical verification iterations from days to under 3 hours, facilitating rapid design-technology co-optimization (DTCO) workflows.
