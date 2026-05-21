---
layout: page
title: Big Data Quantum Mechanics
description: High-throughput Density Functional Theory (DFT) simulations and equivariant GNN modeling for material adsorption energies.
importance: 4
category: academic
img: /assets/img/quantum_mechanics_thumb.png
toc:
  sidebar: left
---

### Project Overview

Discovering novel catalyst materials for chemical synthesis, hydrogen production, and carbon capture requires searching through an astronomical space of alloy configurations and molecular adsorbates. While Density Functional Theory (DFT) provides a quantum-mechanical method to compute adsorption energies, solving these systems scales cubically ($O(N^3)$) with the number of electrons, limiting high-throughput discovery workflows.

This Vertically Integrated Project (VIP) at the Georgia Institute of Technology, supervised by Prof. Andrew J. Medford, utilized high-throughput DFT simulation pipelines and equivariant Graph Neural Networks (GNNs) to create fast, physically-consistent surrogate models for predicting material adsorption properties.

---

### High-Throughput Quantum Espresso Pipelines

To generate dataset samples, we built automated pipelines to execute DFT calculations on high-performance computing (HPC) clusters.

#### 1. Input Deck Generation and Job Automation

We wrote Python wrappers to construct Quantum Espresso input decks. The pipeline:

- Parses molecular structures from ASE (Atomic Simulation Environment) databases.
- Automates boundary cell setups and K-point grids (typically $4 \times 4 \times 1$ for surfaces).
- Generates Slurm batch scripts to distribute calculations across compute nodes.

#### 2. Plane-Wave Cutoff Validation

Calculations utilized Vanderbilt ultrasoft pseudopotentials. We conducted convergence tests to set the kinetic energy cutoff for wavefunctions at $40\text{ Ry}$ and the charge density cutoff at $400\text{ Ry}$, ensuring numerical error in computed energies was below $0.001\text{ Ry}$ per atom.

---

### Kohn-Sham Physics Formulation

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

#### 2. Energy Minimization

The electron density is calculated iteratively until the system energy converges. The final adsorption energy $E_{\text{ads}}$ is:

$$E_{\text{ads}} = E_{\text{slab+adsorbate}} - \left( E_{\text{slab}} + E_{\text{adsorbate}} \right)$$

---

### Equivariant Graph Neural Network (Equiformer_v2)

To bypass expensive DFT relaxation runs, the adsorbate-catalyst system is represented as a 3D molecular graph $G = (V, E)$. To ensure physical consistency, the surrogate network must be equivariant to 3D rotations and translations (the Euclidean group $E(3)$).

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

### Force and Energy Gradient Training

Training only on target energies leads to physical instability during structure relaxation. To address this, we optimized the network to predict atomic forces, which are the negative gradients of the total energy with respect to atomic coordinates:

$$\mathbf{F}_i = -\nabla_{\mathbf{R}_i} E(\mathbf{R}_1, \dots, \mathbf{R}_N)$$

By applying backpropagation through the GNN to calculate the analytical gradient of the predicted energy, we trained the model using a joint loss function:

$$\mathcal{L} = \mathcal{L}_{\text{energy}} + \lambda_{\text{force}} \frac{1}{3N}\sum_{i=1}^{N} \|\mathbf{F}_{i,\text{pred}} - \mathbf{F}_{i,\text{dft}}\|^2$$

where $\lambda_{\text{force}} = 10.0$ balances energy and force training.

---

### Key Outcomes & Technical Impact

- **Database Generation**: Constructed and managed a local database of thousands of relaxed adsorbate-catalyst configurations, modeled after the Open Catalyst Project (OC20) specifications.
- **Model Accuracy**: Achieved a Mean Absolute Error (MAE) of **$0.12\text{ eV}$** in out-of-sample adsorption energy predictions, outperforming classical non-equivariant graph networks (such as CGCNN) by **$45\%$**.
- **Accelerated Screening**: Reduced the calculation time for evaluating candidate catalyst alloy surface sites from several hours (via DFT) to **milliseconds** (via GNN inference), enabling high-speed screening of catalyst spaces.
