---
layout: page
title: Analog IC Design Optimization
description: Automated multi-objective optimization and geometric programming routines for analog integrated circuit sizing.
importance: 9
category: work
img: /assets/img/analog_design_thumb.png
---

### Project Overview

Analog integrated circuit sizing remains one of the most time-consuming steps in semiconductor design. Sizing requires designers to select transistor channel widths ($W$), lengths ($L$), bias currents, and passive component values to meet multiple, competing performance criteria—such as open-loop gain, unity-gain bandwidth, phase margin, power dissipation, and silicon area. Because transistor equations in sub-micron regimes are highly non-linear, designers typically rely on manual, intuitive tweaking and repeated SPICE simulations.

This project developed a design automation framework that formulates transistor sizing as a **Geometric Programming (GP)** problem, enabling the global optimization of analog circuit parameters in milliseconds, verified with a closed-loop SPICE simulation engine.

---

### Geometric Programming (GP) Formulation

Geometric programming is a class of mathematical optimization problems where the objective and constraints are represented as posynomials and monomials. A GP in standard form is written as:

$$
\begin{aligned}
\text{minimize} \quad & f_0(\mathbf{x}) \\
\text{subject to} \quad & f_i(\mathbf{x}) \le 1, \quad i = 1, \dots, m \\
& g_i(\mathbf{x}) = 1, \quad i = 1, \dots, p
\end{aligned}
$$

where $f_0, \dots, f_m$ are posynomials, $g_1, \dots, g_p$ are monomials, and $\mathbf{x} = (x_1, \dots, x_n) > 0$ are the continuous design variables (such as transistor dimensions $W_k, L_k$, and bias currents $I_k$).

#### 1. Posynomial Spec Modeling

To apply GP, performance specifications must be modeled as posynomial functions. For a two-stage Operational Transconductance Amplifier (OTA), the low-frequency open-loop gain $A_v$ is written as:

$$A_v \approx \left(\frac{g_{m2}}{g_{ds2} + g_{ds4}}\right) \left(\frac{g_{m6}}{g_{ds6} + g_{ds7}}\right)$$

where $g_m$ represents transconductance and $g_{ds}$ is the output conductance. By modeling small-signal parameters as monomial fits of layout dimensions:

$$g_{m} \approx \chi \cdot I_D^a \cdot W^b \cdot L^c$$

we formulate the minimum gain constraint ($A_v \ge A_{\text{target}}$) in standard posynomial form:

$$\frac{g_{ds2} + g_{ds4}}{g_{m2}} \cdot \frac{g_{ds6} + g_{ds7}}{g_{m6}} \le \frac{1}{A_{\text{target}}}$$

#### 2. Convex Transformation

By introducing the change of variables $y_i = \ln x_i$, the geometric program is transformed into a convex optimization problem:

$$\text{minimize } \ln f_0(e^\mathbf{y}) \quad \text{subject to } \ln f_i(e^\mathbf{y}) \le 0, \quad \ln g_i(e^\mathbf{y}) = 0$$

which guarantees that any local minimum found is the global optimum.

---

### Closed-Loop SPICE Verification Engine

Because simplified monomial fits do not fully capture second-order short-channel effects (such as drain-induced barrier lowering or velocity saturation), we wrapped the convex solver in a closed-loop refinement loop with Spectre / HSPICE:

```
    Design Specifications (Gain, Bandwidth, Phase Margin)
                            │
                            ▼
               ┌─────────────────────────┐
               │    Posynomial Fitting   │ ◄─── Updates fitting coefficients
               └─────────────────────────┘
                            │
                            ▼
               ┌─────────────────────────┐
               │  Geometric Prog. Solver │
               └─────────────────────────┘
                            │
                            ▼ (Candidate Transistor Sizes)
               ┌─────────────────────────┐
               │     SPICE Simulator     │
               └─────────────────────────┘
                            │
                            ▼ (Actual Specs Evaluated)
             Check if Specs Converged ──► Optimized Design
```

1. **Optimization**: The GP solver computes candidate transistor sizes based on the current posynomial models.
2. **Simulation**: The system auto-generates a SPICE netlist and runs multi-corner AC/transient simulations.
3. **Calibration**: If simulated metrics deviate from model predictions, the fitting coefficients ($\chi, a, b, c$) are re-calibrated around the candidate operating point, and the GP runs again. The loop typically converges within 4–5 iterations.

---

### Key Outcomes & Technical Impact

- **Optimization Speed**: Replaced days of manual transistor sizing with an automated tool that computes optimal parameters for standard amplifiers in under **$2\text{ minutes}$**.
- **Miller OTA Sizing**: Automated the optimization of a two-stage Miller-compensated OTA, achieving **$62\text{ dB}$** gain, **$125\text{ MHz}$** unity-gain bandwidth, and **$63^\circ$** phase margin while reducing power consumption by **$25\%$** compared to human-designed baselines.
- **Robust Yield Sizing**: Integrated multi-corner constraints (evaluating fast/slow corners, temperature extremes from $-40^\circ\text{C}$ to $125^\circ\text{C}$, and supply voltages $\pm10\%$) to guarantee robust parametric yields before layout.
