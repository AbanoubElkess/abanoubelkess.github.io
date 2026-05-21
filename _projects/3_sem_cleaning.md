---
layout: page
title: SEM Image Deep Learning Cleaning
description: Deep neural network pipelines and interactive dashboards to classify, filter, and clean Scanning Electron Microscope (SEM) data for chip metrology.
importance: 3
category: work
area: "Electronic Design Automation (EDA)"
img: /assets/img/sem_cleaning_thumb.png
toc:
  sidebar: left
---

### Project Overview

In semiconductor manufacturing, Critical Dimension Scanning Electron Microscopes (CD-SEMs) are the standard instruments for measuring nano-scale features on silicon wafers. However, raw CD-SEM scans are highly noisy due to charging effects, shot noise from low-dose electron beams (required to prevent resist damage), and physical scanner vibrations. This noise corrupts edge detection, leading to errors in the calibration of Optical Proximity Correction (OPC) models.

This project built a deep-learning-based image cleaning and metrology extraction pipeline. The system filters out unusable images, denoises raw SEM scans, and extracts critical edge dimensions, supported by a custom multi-threaded desktop GUI for data auditing.

---

### Image Noise Modeling in CD-SEM

To clean SEM images, we must model the underlying physical noise processes.

#### 1. Poisson Noise (Shot Noise)

The primary source of high-frequency noise is the statistical variation in the number of secondary electrons detected per pixel. Since the electron dose is minimized to prevent resist shrinkage, the pixel intensities follow a Poisson distribution:

$$P(k \text{ electrons} \mid \lambda) = \frac{\lambda^k e^{-\lambda}}{k!}$$

where $\lambda$ represents the true structural intensity.

#### 2. Charging Effects

As the electron beam scans the wafer, negative charges accumulate on insulated photoresist features, deflecting incoming electrons. This produces slow-frequency intensity drifts and shadow artifacts, which we model as an additive spatial drift term:

$$I_{\text{noisy}}(x, y) = \text{Poisson}\left(I_{\text{clean}}(x, y)\right) + \eta_{\text{charge}}(x, y)$$

---

### Denoising Autoencoder Architecture

The image enhancement system uses a modified U-Net autoencoder with residual skip connections to remove noise while preserving structural edges.

#### 1. Residual Convolutional Blocks

Each layer block in the encoder and decoder contains two $3 \times 3$ convolutional layers followed by Batch Normalization and a LeakyReLU activation. Residual connections bypass the blocks:

$$\mathbf{x}_{l+1} = \text{LeakyReLU}\left( \text{BN}\left( \text{Conv}(\mathbf{x}_l) \right) \right) + \mathbf{x}_l$$

This prevents gradient degradation in deep architectures, preserving sub-nanometer line-edge details.

#### 2. Composite Loss Function

The network is trained using a composite loss function combining Mean Squared Error (MSE) and Structural Similarity Index Measure (SSIM) to preserve sharp boundary gradients:

$$\mathcal{L}_{\text{total}} = (1 - \gamma)\mathcal{L}_{\text{MSE}} + \gamma \left( 1 - \text{SSIM}\left(I_{\text{clean}}, \hat{I}_{\text{clean}}\right) \right)$$

where $\gamma = 0.4$ controls the structural reconstruction weight, and $\text{SSIM}$ evaluates luminance, contrast, and structural similarity over local $11 \times 11$ pixel patches.

---

### Metrology & Contour Fitting Optimization

Once the image is denoised, our engine extracts the boundary coordinates of the resist patterns.

#### 1. Active Contour Fitting (Snakes)

We initialize a parametric contour curve $\mathbf{v}(s) = (x(s), y(s))$ near the denoised edge and minimize its energy functional:

$$E_{\text{snake}} = \int_{0}^{1} \left( E_{\text{internal}}(\mathbf{v}(s)) + E_{\text{external}}(\mathbf{v}(s)) \right) ds$$

where $E_{\text{internal}}$ maintains curve smoothness and $E_{\text{external}} = -\beta \|\nabla \hat{I}_{\text{clean}}(\mathbf{v}(s))\|^2$ pulls the contour toward the steepest image gradients.

#### 2. LER and LWR Formulation

- **Line-Edge Roughness (LER)** is calculated as the $3\sigma$ standard deviation of the edge coordinates $x_i$ from a fitted straight line $\bar{x}$:

  $$\text{LER} = 3 \sqrt{\frac{1}{N} \sum_{i=1}^{N} \left( x_i - \bar{x} \right)^2}$$

- **Line-Width Roughness (LWR)** tracks the variation in local linewidth $w_i$ (distance between left and right contours):

  $$\text{LWR} = 3 \sqrt{\frac{1}{N} \sum_{i=1}^{N} \left( w_i - \bar{w} \right)^2}$$

---

### Multi-Threaded PyQt Visualization Dashboard

To allow calibration engineers to audit the neural network's predictions, we built a cross-platform desktop application using Python, PyQt5, and PySide.

```
┌────────────────────────────────────────────────────────┐
│  PyQt GUI Event Loop (Main Thread - Responsive UI)      │
│     │                                            ▲     │
│     ▼ (Asynchronous QRunnable Job)               │     │
│  ┌───────────────────────────────────────────────┴──┐  │
│  │ QThreadPool Backend (Worker Threads)              │  │
│  │  ├── Thread 1: Async I/O (Load TIFF Images)        │  │
│  │  ├── Thread 2: GPU PyTorch Inference (Denoise)    │  │
│  │  └── Thread 3: Metrology Edge & LER Calculator     │  │
│  └───────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────┘
```

- **Asynchronous QThread Execution**: By dispatching disk I/O and GPU neural network inference to a managed `QThreadPool`, we kept the user interface fully interactive at $60\text{ fps}$ even when processing gigabytes of raw TIFF files.
- **Interactive Annotation**: Integrated interactive canvas tools using `QGraphicsView`, enabling users to adjust metrology search boxes and inspect individual sub-pixel edge points overlaid on the denoised image.

---

### Key Outcomes & Technical Impact

- **Metrology Precision**: Denoised SEM scans achieved a **$15\%$** reduction in CD measurement variance compared to classical Gaussian or median filtering.
- **Workflow Efficiency**: Reduced the manual verification overhead for RET/OPC modeling files by **$30\%$**, replacing manual image categorization with automated deep learning classifiers.
- **Robustness**: Enabled successful metrology extraction on low-contrast, thin-resist nodes that were previously rejected as unmeasurable by classical edge-detection tools.
