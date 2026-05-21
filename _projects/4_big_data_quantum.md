---
layout: page
title: Big Data Quantum Mechanics
description: High-throughput Density Functional Theory (DFT) simulations and equivariant GNN modeling for material adsorption energies.
importance: 4
category: academic
img: /assets/img/quantum_mechanics_thumb.png
---

### Project Overview

Discovering novel catalyst materials for chemical synthesis, hydrogen production, and carbon capture requires searching through an astronomical space of alloy configurations and molecular adsorbates. While Density Functional Theory (DFT) provides a quantum-mechanical method to compute adsorption energies, solving these systems scales cubically ($O(N^3)$) with the number of electrons, limiting high-throughput discovery workflows.

This Vertically Integrated Project (VIP) at the Georgia Institute of Technology, supervised by Prof. Andrew J. Medford, utilized high-throughput DFT simulation pipelines and equivariant Graph Neural Networks (GNNs) to create fast, physically-consistent surrogate models for predicting material adsorption properties.

---

### DFT Physics Formulation

We executed first-principles quantum simulations to establish ground-truth relaxed atomic geometries and adsorption energies.

#### 1. The Kohn-Sham Self-Consistent Field (SCF) Equations

The multi-electron Schrödinger equation is mapped to a system of non-interacting single-particle equations:

$$\left[ -\frac{1}{2}\nabla^2 + V_{\text{eff}}(\mathbf{r}) \right] \psi_i(\mathbf{r}) = \epsilon_i \psi_i(\mathbf{r})$$

where:

- $\psi_i(\mathbf{r})$ represents the single-particle Kohn-Sham wavefunctions.
- $\epsilon_i$ are the energy eigenvalues.
- $V_{\text{eff}}(\mathbf{r})$ is the effective local potential, defined as:

$$V_{\text{eff}}(\mathbf{r}) = V_{\text{ext}}(\mathbf{r}) + \int \frac{n(\mathbf{r}')}{|\mathbf{r} - \mathbf{r}'|} d\mathbf{r}' + V_{\text{xc}}(\mathbf{r})$$

Here, $V_{\text{ext}}$ is the external ionic potential, the integral is the classical Hartree electrostatic potential of the electron density $n(\mathbf{r})$, and $V_{\text{xc}}$ is the exchange-correlation potential, which we modeled using the Generalized Gradient Approximation (GGA-PBE).

#### 2. Simulation Execution

The calculations were run in Quantum Espresso using plane-wave basis sets and Vanderbilt ultrasoft pseudopotentials to model core-electron interactions, relaxing structures until ionic forces fell below $0.01\text{ eV}/\text{Å}$.

---

### Equivariant Graph Neural Network Surrogate (Equiformer_v2)

To replace expensive DFT relaxation runs, the adsorbate-catalyst system is represented as a 3D molecular graph $G = (V, E)$. To ensure physical consistency, the surrogate network must be equivariant to 3D rotations and translations (the Euclidean group $E(3)$).

```
Molecular Graph Nodes (Atoms) & Edges (3D Vectors)
                        │
                        ▼
       ┌─────────────────────────────────┐
       │     Spherical Harmonics Y_lm    │ ──► Captures directional layout geometry
       └─────────────────────────────────┘
                        │
                        ▼
       ┌─────────────────────────────────┐
       │   SO(3)-Equivariant Attention   │ ──► Message passing using Wigner D-matrices
       └─────────────────────────────────┘
                        │
                        ▼
          Adsorption Energy Prediction (eV)
```

- **Wigner Tensor Kernels**: We implemented **Equiformer_v2**, which leverages spherical harmonics $Y_{lm}(\mathbf{\hat{r}}_{ij})$ to represent relative atomic orientations. The message-passing updates node features $h_i$ using irreducible representations (irreps) of the $SO(3)$ rotation group:

$$h_i^{(l+1)} = h_i^{(l)} + \sum_{j \in \mathcal{N}(i)} \text{EquivAttn}\left(h_i^{(l)}, h_j^{(l)}, Y_{lm}(\mathbf{\hat{r}}_{ij})\right)$$

- **Irreps Mapping**: Features are decomposed into scalar (tensor type-0, $l=0$) and vector/tensor components ($l > 0$), allowing the network to track both coordinate-independent quantities (energies) and coordinate-dependent quantities (atomic forces) simultaneously.

---

### Key Outcomes & Technical Impact

- **Database Generation**: Constructed and managed a local database of thousands of relaxed adsorbate-catalyst configurations, modeled after the Open Catalyst Project (OC20) specifications.
- **Model Accuracy**: Achieved a Mean Absolute Error (MAE) of **$0.12\text{ eV}$** in out-of-sample adsorption energy predictions, outperforming classical non-equivariant graph networks (such as CGCNN) by **$45\%$**.
- **Accelerated Screening**: Reduced the calculation time for evaluating candidate catalyst alloy surface sites from several hours (via DFT) to **milliseconds** (via GNN inference), enabling high-speed screening of catalyst spaces.
