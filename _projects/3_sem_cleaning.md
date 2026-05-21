---
layout: page
title: SEM Image Deep Learning Cleaning
description: Deep neural network pipelines and interactive dashboards to classify, filter, and clean Scanning Electron Microscope (SEM) data for chip metrology.
importance: 3
category: work
img: /assets/img/sem_cleaning_thumb.png
---

### Project Overview

In semiconductor manufacturing, Critical Dimension Scanning Electron Microscopes (CD-SEMs) are the standard instruments for measuring nano-scale features on silicon wafers. However, raw CD-SEM scans are highly noisy due to charging effects, shot noise from low-dose electron beams (required to prevent resist damage), and physical scanner vibrations. This noise corrupts edge detection, leading to errors in the calibration of Optical Proximity Correction (OPC) models.

This project built a deep-learning-based image cleaning and metrology extraction pipeline. The system filters out unusable images, denoises raw SEM scans, and extracts critical edge dimensions, supported by a custom multi-threaded desktop GUI for data auditing.

---

### Denoising Architecture & Metrology Formulation

The image enhancement system uses a two-stage computer vision pipeline: an image-to-image denoising network and a contour extraction optimizer.

#### 1. U-Net Denoising Autoencoder

To reconstruct clean, high-contrast structural boundaries from noisy scans, we deployed a modified U-Net autoencoder with residual connections. The network learns a mapping $f_{\theta}$ from the noisy input image $I_{\text{noisy}}$ to a clean approximation $\hat{I}_{\text{clean}}$:

$$\hat{I}_{\text{clean}} = f_{\theta}(I_{\text{noisy}})$$

The model is trained using a composite loss function combining Mean Squared Error (MSE) and Structural Similarity Index Measure (SSIM) to preserve critical boundary edges:

$$\mathcal{L}_{\text{total}} = (1 - \gamma)\mathcal{L}_{\text{MSE}} + \gamma \left( 1 - \text{SSIM}\left(I_{\text{clean}}, \hat{I}_{\text{clean}}\right) \right)$$

where $\gamma = 0.4$ controls the structural reconstruction weight.

#### 2. Line-Edge Roughness (LER) Formulation

Once the image is denoised, our engine extracts the boundary coordinates of the resist patterns. Line-Edge Roughness (LER), a critical metric for semiconductor yields, is calculated as the $3\sigma$ standard deviation of the edge coordinates $x_i$ from a fitted straight line $\bar{x}$:

$$\text{LER} = 3 \sqrt{\frac{1}{N} \sum_{i=1}^{N} \left( x_i - \bar{x} \right)^2}$$

This calculation is performed dynamically along the feature length, enabling sub-nanometer metrology tracking.

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

- **Asynchronous Execution**: By dispatching image reading, GPU neural network inference, and contour fitting to a managed `QThreadPool`, we kept the user interface fully interactive at $60\text{ fps}$ even when processing gigabytes of raw TIFF files.
- **Interactive Annotation**: Integrated interactive canvas tools using `QGraphicsView`, enabling users to adjust metrology search boxes and inspect individual sub-pixel edge points overlaid on the denoised image.

---

### Key Outcomes & Technical Impact

- **Metrology Precision**: Denoised SEM scans achieved a **$15\%$** reduction in CD measurement variance compared to classical Gaussian or median filtering.
- **Workflow Efficiency**: Reduced the manual verification overhead for RET/OPC modeling files by **$30\%$**, replacing manual image categorization with automated deep learning classifiers.
- **Robustness**: Enabled successful metrology extraction on low-contrast, thin-resist nodes that were previously rejected as unmeasurable by classical edge-detection tools.
