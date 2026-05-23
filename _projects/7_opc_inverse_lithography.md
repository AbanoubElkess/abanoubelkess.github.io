---
layout: page
title: OPC & Inverse Lithography
description: GPU-accelerated Inverse Lithography Technology (ILT) and model-based Optical Proximity Correction (OPC) optimization for sub-14nm semiconductor manufacturing nodes.
importance: 7
category: work
area: "Electronic Design Automation (EDA)"
img: /assets/img/opc_lithography_thumb.png
toc:
  sidebar: left
---

### Project Overview

In advanced semiconductor manufacturing nodes (sub-14nm), the wavelength of light used in deep ultraviolet (DUV) photolithography ($193\text{ nm}$ argon fluoride immersion lasers) is significantly larger than the target feature sizes printed on the silicon wafer. As light passes through the scanner's projection system and photomask, severe diffraction and chemical process distortions occur. These optical distortions lead to structural defects such as line-end shortening, corner rounding, pattern merging, and overall yield loss.

To address these physical limits, we developed a GPU-accelerated **Inverse Lithography Technology (ILT)** and **Model-Based Optical Proximity Correction (OPC)** engine. The software treats mask synthesis as a mathematical inverse problem. By modeling the forward optical and photoresist physics, the engine optimizes the photomask layout to minimize the discrepancy between the printed wafer contours and the target integrated circuit design.

<div class="row justify-content-sm-center">
  <div class="col-sm-8 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/opc_lithography_thumb.png" title="OPC and Inverse Lithography Technology" class="img-fluid rounded z-depth-1" zoomable=true caption="Figure 1: Inverse lithography optimization process from mask design to wafer print simulation." %}
  </div>
</div>

---

### Forward Lithography Modeling

The forward simulation pipeline models how light propagates through the optical projection system and how the photoresist layer reacts to the incident light intensity.

```
       ┌───────────────────────────────┐
       │   Target Mask Layout M(x, y)  │
       └───────────────┬───────────────┘
                       │
                       ▼ (Coherent Kernel Decomposition)
       ┌───────────────────────────────┐
       │  Hopkins Optical Model H_k    │ ──► Compute Aerial Image I(x, y)
       └───────────────┬───────────────┘
                       │
                       ▼ (Sigmoid Threshold Reaction)
       ┌───────────────────────────────┐
       │     Photoresist Model W(x, y) │ ──► Compute Final Wafer Contour
       └───────────────┬───────────────┘
                       │
                       ▼ (Edge Placement Error Evaluation)
       ┌───────────────────────────────┐
       │  L2 Loss & Gradient Optimizer  │ ──► Backpropagate to Update Mask M
       └───────────────────────────────┘
```

#### 1. The Hopkins Diffraction Model

We model the light intensity profile at the wafer plane, known as the aerial image $I(x, y)$, using Hopkins' theory of partially coherent imaging. The partially coherent optical system is represented by the transmission cross-coefficient (TCC) matrix. We perform a Singular Value Decomposition (SVD) on the TCC matrix to decompose the partially coherent system into a sum of coherent systems (the Optimal Coherent Approximation, or OCA):

$$I(x, y) = \sum_{k=1}^{N_c} \lambda_k \left| \left( M * H_k \right)(x, y) \right|^2$$

where:

- $M(x, y) \in [0, 1]^2$ is the continuous mask transmission function ($1$ for clear quartz, $0$ for chrome).
- $H_k(x, y)$ are the coherent kernels representing the scanner's pupil function, numerical aperture (NA), and illumination source.
- $\lambda_k$ is the eigenvalue associated with the $k$-th coherent kernel, indicating its relative energy contribution.
- $*$ denotes the 2D spatial convolution operation.
- $N_c$ is the truncation order (typically $N_c = 5$ to $10$), balancing simulation accuracy and runtime.

#### 2. The Photoresist Reaction Model

Once the aerial image $I(x, y)$ is computed, we model the chemical response of the photoresist during the exposure and post-exposure bake (PEB) steps. The concentration of photo-acid generators and the subsequent development process are approximated using a continuous, differentiable sigmoid function:

$$W(x, y) = \frac{1}{1 + \exp\left(-\alpha \left(I(x, y) - I_{th}\right)\right)}$$

where:

- $W(x, y) \in [0, 1]$ represents the local resist development probability (where $W \ge 0.5$ designates dissolved resist, representing the final wafer contour).
- $I_{th}$ is the threshold intensity parameter determined by process calibration.
- $\alpha$ is the scaling factor modeling the contrast of the chemical photoresist formulation.

---

### GPU-Accelerated Inverse Lithography Formulation (ILT)

We formulate mask synthesis as a high-dimensional, non-convex optimization problem over the continuous mask pixel grid $M(x, y)$.

#### 1. Objective Function

The goal is to find a mask $M(x, y)$ that minimizes the difference between the simulated wafer contour $W(x, y)$ and the target circuit design $T(x, y)$ while maintaining manufacturability:

$$\mathcal{J}(M) = \iint_{\Omega} \left( W(x, y) - T(x, y) \right)^2 dx\,dy + \gamma_{\text{TV}} \mathcal{R}_{\text{TV}}(M) + \gamma_{\text{tone}} \mathcal{R}_{\text{tone}}(M)$$

where:

- $\mathcal{R}_{\text{TV}}(M)$ is the Total Variation (TV) regularization term, which suppresses high-frequency noise and prevents the optimizer from generating fragmented, unmanufacturable shapes:

  $$\mathcal{R}_{\text{TV}}(M) = \iint_{\Omega} \sqrt{\left(\frac{\partial M}{\partial x}\right)^2 + \left(\frac{\partial M}{\partial y}\right)^2} dx\,dy$$

- $\mathcal{R}_{\text{tone}}(M) = \iint_{\Omega} M^2(1 - M)^2 dx\,dy$ is a tone-consistency penalty that forces the optimized mask pixels to converge to binary values ($0$ or $1$) at the end of the optimization process.
- $\gamma_{\text{TV}}$ and $\gamma_{\text{tone}}$ are weighting hyperparameters.

#### 2. CUDA-Accelerated Gradient Optimization

Because the forward model is composed of differentiable operations (convolutions and element-wise functions), we compute the analytical gradient of the objective function with respect to the mask layout $\nabla_M \mathcal{J}$ using backpropagation.

We implemented the optimization framework in PyTorch with custom CUDA-accelerated convolution kernels. The optimization updates the mask iteratively using a gradient-descent optimizer with momentum (such as Adam):

$$M^{(l+1)} = \text{clip}\left( M^{(l)} - \eta \cdot \text{Adam}\left(\nabla_{M^{(l)}} \mathcal{J}\right), 0, 1 \right)$$

By executing the multi-channel 2D convolutions ($M * H_k$) in parallel on GPU tensor cores, we accelerate the gradient calculation steps.

---

### Sub-Resolution Assist Feature (SRAF) Generation

Sub-Resolution Assist Features (SRAFs) are narrow geometries placed on the mask that do not print on the wafer themselves but help collect diffracted light to improve the depth of focus and process window of the target features.

```
       ┌────────────────────────────────────────────────────────┐
       │ Optimized Continuous Pixel Mask Solution M(x, y)       │
       └──────────────────────────┬─────────────────────────────┘
                                  │
                                  ▼
       ┌────────────────────────────────────────────────────────┐
       │ Threshold and Segment into Candidate SRAF Regions      │
       └──────────────────────────┬─────────────────────────────┘
                                  │
                                  ▼
       ┌────────────────────────────────────────────────────────┐
       │ Apply Mask Rule Checks (MRC) & Snap to Rectangles      │
       │  - Min Width, Min Spacing, and Manhattan Alignments    │
       └──────────────────────────┬─────────────────────────────┘
                                  │
                                  ▼
       ┌────────────────────────────────────────────────────────┐
       │ Final Manufacturable Mask with Clean, Discrete SRAFs   │
       └────────────────────────────────────────────────────────┘
```

1. **Continuous SRAF Detection**: The continuous-pixel optimization naturally develops low-intensity, isolated bands around primary features, which act as model-based assist features.
2. **Geometrical Fitting**: The continuous mask representation is segmented into isolated regions. These regions are fitted with rectangular shapes using custom polygon-extraction algorithms.
3. **Mask Rule Check (MRC) Alignment**: The fitted rectangles are snapped to a grid and verified against manufacturing constraints (e.g., minimum SRAF width and minimum spacing between SRAFs and main features), ensuring the mask can be manufactured by standard electron-beam mask writers.

---

### Experimental Results & Verification

The ILT engine was benchmarked on representative sub-14nm logic layouts (including dense contact holes and metal lines) using physical process parameters.

#### 1. Lithography Quality Metrics

We evaluated the quality of the printed patterns across three metrics: Edge Placement Error (EPE), Common Process Window (PV band area), and Mask Error Enhancement Factor (MEEF).

| Layout Type              |    Metric    | Conventional OPC  | Model-Based ILT (Ours) | Improvement |
| :----------------------- | :----------: | :---------------: | :--------------------: | :---------: |
| **Metal Line (Dense)**   |   Max EPE    |  $4.2\text{ nm}$  |  **$1.8\text{ nm}$**   |    57.1%    |
|                          | PV Band Area | $112\text{ nm}^2$ |  **$68\text{ nm}^2$**  |    39.3%    |
| **Contact Hole (Array)** |   Max EPE    |  $3.5\text{ nm}$  |  **$1.2\text{ nm}$**   |    65.7%    |
|                          |     MEEF     |        3.8        |        **2.1**         |    44.7%    |

- **EPE Reduction**: Across all test patterns, the continuous pixel-level ILT engine reduced the maximum Edge Placement Error by over **$50\%$**, ensuring that the printed shapes matched the target layout geometries within tolerances.
- **Process Window Stability**: The common depth of focus (DoF) increased by **$35\%$**, indicating that the optimized mask layout maintains pattern fidelity even under focal-plane drift and exposure dose fluctuations inside the scanner.

#### 2. GPU Speedup Benchmarks

We measured the execution runtime of the optimization loop for a standard $100\mu\text{m} \times 100\mu\text{m}$ layout block:

- **CPU-only Baseline (Intel Xeon 24-core)**: $34.5\text{ minutes}$
- **GPU-accelerated ILT (Single NVIDIA RTX 4090)**: **$2.7\text{ minutes}$**
- **Multi-GPU Scaling (4 $\times$ NVIDIA H100)**: **$42\text{ seconds}$** ($49\times$ total speedup)

This acceleration makes full-chip model-based ILT runs computationally feasible within production timeline schedules.
