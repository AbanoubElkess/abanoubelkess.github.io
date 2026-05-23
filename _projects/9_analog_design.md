---
layout: page
title: Analog IC Design Optimization
description: Automated multi-objective optimization and geometric programming routines for analog integrated circuit sizing.
importance: 9
category: work
area: "Electronic Design Automation (EDA)"
img: /assets/img/analog_design_thumb.png
toc:
  sidebar: left
---

### Project Overview

Analog integrated circuit (IC) sizing is one of the most time-consuming steps in semiconductor design. Choosing transistor channel widths ($W$), lengths ($L$), bias currents, and passive component values is a challenging task. Designers must balance multiple competing performance specifications—such as low-frequency open-loop gain, unity-gain bandwidth, phase margin, power dissipation, noise, and silicon area. Because transistor behaviors in sub-micron regimes are highly non-linear, designers typically rely on manual sizing and iterative SPICE simulations.

To address these challenges, we built an automated design framework that formulates transistor sizing as a **Geometric Programming (GP)** problem. By modeling performance metrics as posynomial functions and coupling the optimization with a closed-loop SPICE simulation engine, the framework sizing circuit parameters in seconds while ensuring physical accuracy.

<div class="row justify-content-sm-center">
  <div class="col-sm-8 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/analog_design_thumb.png" title="Analog IC Design Schematic" class="img-fluid rounded z-depth-1" zoomable=true caption="Figure 1: Operational Transconductance Amplifier (OTA) circuit schematic and design optimization parameter mappings." %}
  </div>
</div>

---

### Geometric Programming (GP) Formulation

Geometric programming is a class of mathematical optimization problems characterized by objective functions and constraints expressed as posynomials and monomials.

#### 1. Monomial and Posynomial Definitions

Let $\mathbf{x} = (x_1, x_2, \dots, x_n)$ be a vector of $n$ real, positive variables.

- A **monomial** function $g(\mathbf{x})$ is defined as:

  $$g(\mathbf{x}) = c x_1^{a_1} x_2^{a_2} \dots x_n^{a_n}$$

  where $c > 0$ and $a_i \in \mathbb{R}$.

- A **posynomial** function $f(\mathbf{x})$ is a sum of one or more monomials:

  $$f(\mathbf{x}) = \sum_{k=1}^K c_k x_1^{a_{1k}} x_2^{a_{2k}} \dots x_n^{a_{nk}}$$

  where $c_k > 0$.

A GP in standard form is written as:

$$
\begin{aligned}
\text{minimize} \quad & f_0(\mathbf{x}) \\
\text{subject to} \quad & f_i(\mathbf{x}) \le 1, \quad i = 1, \dots, m \\
& g_i(\mathbf{x}) = 1, \quad i = 1, \dots, p
\end{aligned}
$$

where $f_0, \dots, f_m$ are posynomials and $g_1, \dots, g_p$ are monomials.

#### 2. Convex Transformation

By introducing a change of variables $y_i = \ln x_i$ and taking the natural logarithm of the functions, the geometric program is transformed into a convex optimization problem:

$$\text{minimize } \ln f_0(e^\mathbf{y}) \quad \text{subject to } \ln f_i(e^\mathbf{y}) \le 0, \quad \ln g_i(e^\mathbf{y}) = 0$$

Because the transformed objective function is convex and the constraint set is convex, any local minimum is guaranteed to be the global optimum. We solve this transformed problem using interior-point numerical methods.

---

### Performance Characterization for a Two-Stage Miller OTA

To apply GP to an operational transconductance amplifier (OTA), we express its small-signal parameters and design constraints in terms of transistor dimensions.

```
                  VDD
                   │
           ┌───────┴───────┐
         M3│             M4│
           ├───────┬───────┤
           │       │       │
           ├───M1  M2──┐   │
         In+   │   │   In- │
               └───┬───┘   ├───M6─── Out
                 M5│       │
                   └───┬───┘
                       │   M7
                      VSS
```

#### 1. Small-Signal Transistor Monomial Fits

In sub-micron processes, classical square-law models ($I_D \propto W/L (V_{gs}-V_{th})^2$) do not capture short-channel effects like velocity saturation. We model small-signal characteristics ($g_m$, $g_{ds}$, and capacitances $C_{gg}, C_{gd}$) as monomial functions fitted over SPICE look-up tables:

$$g_{m} \approx \chi \cdot I_D^a \cdot W^b \cdot L^c$$

$$g_{ds} \approx \zeta \cdot I_D^d \cdot W^e \cdot L^f$$

where $\chi, \zeta$ and the exponents $a, b, c, d, e, f$ are fitting parameters optimized for specific bias regions.

#### 2. Sizing Constraints Formulation

Using these monomial fits, we formulate the amplifier specifications:

- **Open-Loop Gain ($A_v$)**:

  $$A_v \approx \left(\frac{g_{m2}}{g_{ds2} + g_{ds4}}\right) \left(\frac{g_{m6}}{g_{ds6} + g_{ds7}}\right)$$

  We express the constraint $A_v \ge A_{\text{target}}$ as a posynomial inequality:

  $$\frac{g_{ds2} + g_{ds4}}{g_{m2}} \cdot \frac{g_{ds6} + g_{ds7}}{g_{m6}} \le \frac{1}{A_{\text{target}}}$$

- **Unity-Gain Bandwidth ($GBW$)**:

  $$GBW = \frac{g_{m1}}{C_c} \ge GBW_{\text{target}} \implies \frac{GBW_{\text{target}} \cdot C_c}{g_{m1}} \le 1$$

- **Phase Margin ($PM$)**:
  To ensure stability, the non-dominant pole $p_2 \approx \frac{g_{m6}}{C_L}$ is constrained relative to the unity-gain frequency:

  $$p_2 \ge \eta \cdot GBW \implies \frac{\eta \cdot g_{m1} \cdot C_L}{g_{m6} \cdot C_c} \le 1$$

  where $\eta \approx 3.0$ enforces a phase margin of $\ge 60^\circ$ under a capacitive load $C_L$.

---

### Closed-Loop SPICE Verification & Calibration

Because local monomial fits can deviate from actual behavior across wide sizing ranges, we wrap the GP solver in an automated calibration loop with the SPICE simulator.

```
       ┌────────────────────────────────────────────────────────┐
       │ Inputs: Target Specifications & Initial Monomial Models │
       └──────────────────────────┬─────────────────────────────┘
                                  │
                                  ▼
       ┌────────────────────────────────────────────────────────┐
       │ Run Convex Geometric Programming (GP) Solver           │
       └──────────────────────────┬─────────────────────────────┘
                                  │
                                  ▼ (Candidate W, L, I_D)
       ┌────────────────────────────────────────────────────────┐
       │ Generate Netlist & Execute SPICE (Spectre/HSPICE)      │
       └──────────────────────────┬─────────────────────────────┘
                                  │
                                  ▼ (Extract actual performance)
       ┌────────────────────────────────────────────────────────┐
       │ Verify Convergence: Do simulated specs match targets?  │
       └──────────────────────────┬─────────────────────────────┘
                     No           │           Yes
         ┌────────────────────────┴────────┐  │
         ▼ (Adjust Fitting Coefficients)   ▼  ▼
   Update Monomial Fits Around       [ Sizing Converged! ]
   Candidate Operating Point
```

1. **GP Execution**: The optimization engine solves the convex GP problem using the current monomial model coefficients.
2. **Netlist Generation & SPICE Simulation**: The candidate sizing variables ($W_i, L_i, I_{D,i}$) are written to a SPICE netlist template. The system runs multi-corner AC and transient simulations using Spectre or HSPICE.
3. **Mismatch Extraction & Model Calibration**: The framework compares the simulated performance metrics against the GP model predictions. If the errors exceed $1\%$, it updates the local fitting coefficients ($\chi, \zeta, a, b, \dots$) around the candidate sizing point using a local Jacobian matrix, and re-runs the GP solver. This loop typically converges in 3 to 5 iterations.

---

### Experimental Results & Verification

We sized a two-stage Miller-compensated OTA in a $65\text{ nm}$ CMOS process node, targeting a load capacitance $C_L = 5\text{ pF}$.

#### 1. Performance Comparison

The table below compares the GP-optimized design against a manual design created by an experienced engineer:

| Parameter                |    Specifications    |    Manual Design     |           GP-Optimized (Ours)            |
| :----------------------- | :------------------: | :------------------: | :--------------------------------------: |
| **Open-Loop Gain**       |  $\ge 60\text{ dB}$  |   $61.2\text{ dB}$   |           **$62.5\text{ dB}$**           |
| **Unity-Gain Bandwidth** | $\ge 100\text{ MHz}$ |   $105\text{ MHz}$   |           **$124\text{ MHz}$**           |
| **Phase Margin**         |    $\ge 60^\circ$    |     $61.5^\circ$     |             **$63.2^\circ$**             |
| **Power Dissipation**    |       Minimize       |   $1.42\text{ mW}$   |  **$1.06\text{ mW}$** (25.3% reduction)  |
| **Silicon Area**         |       Minimize       |  $340\mu\text{m}^2$  | **$210\mu\text{m}^2$** (38.2% reduction) |
| **Execution Time**       |          -           | $\sim 2\text{ days}$ |         **$1.8\text{ minutes}$**         |

#### 2. Robust Multi-Corner Sizing

To ensure manufacturing yield, the GP formulation incorporated multi-corner design constraints:

- **Process Corners**: Evaluated across Slow-Slow (SS), Fast-Fast (FF), and Typical-Typical (TT) transistor corners.
- **Temperature Extremes**: Constrained to meet specifications from $-40^\circ\text{C}$ to $125^\circ\text{C}$.
- **Supply Voltage Corners**: Evaluated under $V_{DD} \pm 10\%$.
- The optimizer identified a sizing solution that satisfied the minimum phase margin ($60^\circ$) and gain ($60\text{ dB}$) across all PVT corners.
