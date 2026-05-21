---
layout: page
title: ML TCAD Process Modeling
description: Neural-network surrogates for semiconductor process simulation (etch, deposition, CMP), accelerating TCAD workflows by 100x.
importance: 8
category: work
img: /assets/img/process_modeling_thumb.png
---

### Project Overview

Technology Computer-Aided Design (TCAD) process simulation is essential for exploring the fabrication steps of modern semiconductor structures (such as FinFETs and Gate-All-Around nanosheets). However, traditional TCAD tools rely on solving complex, coupled Partial Differential Equations (PDEs) for gas-phase transport, surface reactions, and level-set profile evolution. These physical simulations take hours to run, creating a bottleneck for design-technology co-optimization (DTCO).

In this project, we built **Physics-Informed Neural Network (PINN)** and **Fourier Neural Operator (FNO)** surrogate models. These models map layout geometry and process parameters directly to post-fabrication profiles, accelerating simulation speed while retaining physical accuracy.

---

### Machine Learning TCAD Architecture

The core objective is to replace traditional level-set numerical PDE solvers with a deep neural operator that predicts the material boundary evolution over time.

```
Layout Geometry (2D/3D Mesh)  +  Process Recipe Vector (Gas Flow, Temp, Pressure, Time)
                    │
                    ▼
     ┌─────────────────────────────┐
     │   Fourier Neural Operator   │  ◄── Guided by Physics-Informed Constraints
     │            (FNO)            │      (Conservation of volume, boundary continuity)
     └─────────────────────────────┘
                    │
                    ▼
        Post-Process Profile Contour
```

#### 1. Fourier Neural Operator (FNO) Formulation

We model the etch rate and deposition profiles by learning the mapping between infinite-dimensional function spaces. The FNO learns the operator by parameterized integral kernels in Fourier space:

$$u_{l+1}(x) = \sigma \left( W u_l(x) + \mathcal{F}^{-1} \left( R_l \cdot \mathcal{F}(u_l) \right)(x) \right)$$

where:

- $\mathcal{F}$ and $\mathcal{F}^{-1}$ represent the Forward and Inverse Fourier Transforms.
- $R_l$ is a tensor of learnable complex parameter weights in the Fourier domain that filters out high-frequency spatial noise.
- $W$ is a linear local transformation.
- $\sigma$ is a non-linear activation function.

#### 2. Physics-Informed Constraints (PINN Loss)

To prevent non-physical predictions (such as material creation out of empty space or discontinuous boundaries), we enforce volume conservation and directional etch constraints in the loss function:

$$\mathcal{L} = \mathcal{L}_{\text{data}} + \beta_1 \mathcal{L}_{\text{conservation}} + \beta_2 \mathcal{L}_{\text{boundary}}$$

where:

- $\mathcal{L}_{\text{data}} = \frac{1}{N}\sum |u_{\text{pred}} - u_{\text{tcad}}|^2$ is the mean-squared error.
- $\mathcal{L}_{\text{conservation}}$ penalizes violations of mass conservation during etching and deposition.
- $\mathcal{L}_{\text{boundary}}$ ensures spatial continuity of material interfaces.

---

### Key Outcomes & Technical Impact

- **$120\times$ Speedup**: Predicted 3D etching profiles for high-aspect-ratio trenches in **milliseconds** instead of minutes, enabling rapid DTCO iterations.
- **Recipe Optimization**: Integrated the FNO surrogate with a Particle Swarm Optimization (PSO) framework. This allowed us to automatically optimize gas flow ratios and RF bias power recipes to achieve target sidewall angles ($90^\circ \pm 0.2^\circ$).
- **Silicon Calibration**: Calibrated the model outputs against experimental Scanning Electron Microscope (SEM) cross-sections, closing the gap between idealized TCAD and real wafer profiles.
