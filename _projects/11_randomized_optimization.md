---
layout: page
title: Randomized Optimization & Clustering Benchmarks
description: Comparative analysis of randomized search heuristics and unsupervised learning algorithms across discrete optimization spaces and high-dimensional clustering problems.
importance: 11
category: academic
area: "Machine Learning & Data Science"
img: /assets/img/optimization_curves.png
toc:
  sidebar: left
---

### Project Overview

This project presents a multi-part empirical study covering two core domains in machine learning: randomized optimization heuristics and unsupervised learning/dimensionality reduction. The first phase evaluates randomized search algorithms for direct weight optimization in neural networks and discrete optimization problems. The second phase analyzes the performance and structural preservation of clustering algorithms when paired with various dimensionality reduction projections.

---

### Part I: Randomized Optimization Heuristics

Traditional gradient-based methods (e.g., Backpropagation) require differentiable loss landscapes. When optimizing non-differentiable or highly complex discrete loss surfaces, randomized search heuristics provide robust alternatives. We analyze four key algorithms.

#### 1. Simulated Annealing (SA)

To escape local minima, Simulated Annealing accepts downhill moves with a probability that decreases over time. The acceptance probability for a candidate state with energy $E_{\text{candidate}}$ relative to the current state $E_{\text{current}}$ is given by:

$$P(\text{accept}) = \exp\left(-\frac{\Delta E}{T}\right)$$

where $\Delta E = E_{\text{candidate}} - E_{\text{current}} > 0$. The temperature parameter $T$ decays according to a geometric cooling schedule:

$$T_k = T_0 \cdot \alpha^k$$

with decay constant $\alpha \in (0.9, 0.99)$.

#### 2. Mutual-Information-Maximizing Input Clustering (MIMIC)

MIMIC models the search space by fitting a probability distribution over the top $\theta$-percentile of candidate solutions. It constructs a dependency tree representing the joint distribution, optimizing the selection of parent variables to minimize the Kullback-Leibler (KL) divergence to the target distribution:

$$P(X_1, X_2, \dots, X_n) = P(X_{i_1}) \prod_{j=2}^{n} P(X_{i_j} \mid X_{i_{\pi(j)}})$$

where $\pi(j)$ represents the parent node of index $j$ in the spanning tree structure.

#### 3. Empirical Optimization Benchmarks

The heuristics were evaluated on three discrete spaces: Continuous Peaks, FlipFlop, and Knapsack. The performance curves illustrate the efficiency of population-based heuristics (Genetic Algorithms and MIMIC) in scaling to high-dimensional spaces compared to local search heuristics (RHC and SA).

---

### Part II: Clustering & Dimensionality Reduction

Unsupervised learning workflows are evaluated by combining clustering partitions with dimensionality reduction algorithms to process complex high-dimensional datasets.

#### 1. Expectation-Maximization (EM) for Gaussian Mixture Models (GMM)

Unlike the hard partitions of K-Means, GMMs provide probabilistic soft assignments. The Expectation step computes the posterior probability (responsibility) of cluster $k$ for data point $\mathbf{x}_i$:

$$\gamma_{ik} = \frac{\pi_k \mathcal{N}(\mathbf{x}_i \mid \boldsymbol{\mu}_k, \boldsymbol{\Sigma}_k)}{\sum_{j=1}^{K} \pi_j \mathcal{N}(\mathbf{x}_i \mid \boldsymbol{\mu}_j, \boldsymbol{\Sigma}_j)}$$

The Maximization step updates the parameters $\pi_k$, $\boldsymbol{\mu}_k$, and $\boldsymbol{\Sigma}_k$ using these responsibilities.

#### 2. Dimensionality Reduction Methods

The study systematically evaluates the preservation of cluster structures across four dimensionality reduction techniques:

- **Principal Component Analysis (PCA)**: Linear projection that maximizes variance by solving the eigenvalue problem for the sample covariance matrix $\boldsymbol{\Sigma}$:
  $$\boldsymbol{\Sigma} \mathbf{v} = \lambda \mathbf{v}$$
- **Independent Component Analysis (ICA)**: Source separation technique maximizing non-Gaussianity via FastICA approximations of negentropy.
- **Randomized Projections (RP)**: Dimension reduction using random matrices, preserving pairwise Euclidean distances within $\epsilon$ error as bounded by the Johnson-Lindenstrauss lemma:
  $$(1-\epsilon)\|\mathbf{u}-\mathbf{v}\|^2 \le \|f(\mathbf{u}) - f(\mathbf{v})\|^2 \le (1+\epsilon)\|\mathbf{u}-\mathbf{v}\|^2$$

---

### Reference Materials & PDF Downloads

For detailed reports, complete with convergence proofs, hyperparameter tuning tables, and comparative visualizations across multiple datasets, you can download the project reports:

- [Randomized Optimization Report (PDF)](/assets/pdf/CS7641_ML_Randomized_Optimization_Su24.pdf)
- [Supervised Learning Benchmarks Report (PDF)](/assets/pdf/CS7641_ML_Supervised_Learning___Su24.pdf)
- [Unsupervised Learning & Dimensionality Reduction Report (PDF)](/assets/pdf/CS7641_ML_Unsupervised_Learning___Su24.pdf)
