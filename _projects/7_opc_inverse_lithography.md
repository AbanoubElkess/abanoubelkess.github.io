---
layout: page
title: OPC & Inverse Lithography
description: GPU-accelerated Inverse Lithography Technology (ILT) and model-based Optical Proximity Correction (OPC) optimization for sub-14nm semiconductor manufacturing nodes.
importance: 7
category: work
img: /assets/img/opc_lithography_thumb.png
---

### Project Overview

In sub-14nm semiconductor manufacturing nodes, the wavelength of light used in deep ultraviolet (DUV) photolithography ($193\text{ nm}$ immersion) is significantly larger than the target feature sizes on the silicon wafer. Consequently, severe diffraction and process distortions occur, leading to structural failures such as line-end shortening, corner rounding, and pattern merging.

To resolve these errors, this project developed a GPU-accelerated **Inverse Lithography Technology (ILT)** and **Model-based Optical Proximity Correction (OPC)** engine. The software mathematically distorts the photomask layout to ensure that the printed patterns on the wafer exactly match the desired IC layout.

---

### Physical Modeling & Mathematical Formulation

The forward lithography process consists of two primary models: an optical model simulating light propagation through the scanner projection system, and a resist model simulating the chemical response of the photoresist.

#### 1. The Forward Optical Model (Hopkins Diffraction)

We model the light intensity profile at the wafer plane, known as the aerial image $I(x, y)$, using Hopkins' theory of partially coherent imaging. By performing singular value decomposition (SVD) on the Transmission Cross-Coefficient (TCC) matrix, the partially coherent system is decomposed into a sum of coherent systems (the Optimal Coherent Approximation, or OCA):

$$I(x, y) = \sum_{k=1}^{N} \lambda_k \left| \left( M * H_k \right)(x, y) \right|^2$$

where:

- $M(x, y) \in [0, 1]^2$ is the continuous mask transmission function.
- $H_k(x, y)$ are the coherent kernels representing the optical system.
- $\lambda_k$ are the eigenvalues of the TCC decomposition.
- $*$ denotes 2D spatial convolution.

#### 2. The Photoresist Model

To determine the final printed wafer contour, we model the chemical threshold reaction of the photoresist using a continuous sigmoid function:

$$W(x, y) = \frac{1}{1 + \exp\left(-\alpha \left(I(x, y) - I_{th}\right)\right)}$$

where $I_{th}$ is the threshold intensity and $\alpha$ controls the slope of the resist transition.

---

### Optimization Framework

The mask design is treated as a high-dimensional non-linear inverse problem. The goal is to optimize the mask transmission grid $M(x, y)$ to minimize the discrepancy between the printed wafer contour $W(x, y)$ and the target layout design $T(x, y)$:

$$\mathcal{J}(M) = \iint_{\Omega} \left( W(x, y) - T(x, y) \right)^2 dx\,dy + \gamma \mathcal{R}(M)$$

#### Regularization for Manufacturability

To ensure the optimized mask is manufacturable by electron-beam mask writers, we append a Total Variation (TV) regularization penalty $\mathcal{R}(M)$, which suppresses high-frequency noise and prevents the formation of isolated, unresolvable sub-resolution assist features (SRAFs):

$$\mathcal{R}(M) = \iint_{\Omega} \sqrt{\left(\frac{\partial M}{\partial x}\right)^2 + \left(\frac{\partial M}{\partial y}\right)^2} dx\,dy$$

We solved this non-convex minimization problem using **gradient descent with backpropagation** implemented in PyTorch, leveraging CUDA-accelerated convolutions to calculate the analytical gradients $\frac{\partial \mathcal{J}}{\partial M}$ in parallel.

---

### Key Outcomes & Technical Impact

- **GPU Acceleration**: Reduced the computation time for full-chip ILT mask synthesis by **$12\times$**, cutting run times from days to under 3 hours per layout block.
- **EPE Reduction**: Decreased the Edge Placement Error (EPE) across critical dense layout patterns by **$18\%$**.
- **Assist Feature Optimization**: Integrated an automated rule-based filter that converts continuous-valued mask solutions into clean, rectangular, manufacturable SRAFs, ensuring compliance with mask inspection tools.
