---
layout: post
title: "Unsupervised Learning: Clustering and Dimensionality Reduction in High-Noise Domains"
date: 2024-07-25
categories: machine-learning
description: "Benchmarking K-Means, Expectation Maximization, PCA, ICA, and Randomized Projections, and their integration as feature generators for Neural Network classifiers."
related_posts: false
chart:
  plotly: true
---

In machine learning, high-dimensional datasets and noise represent major challenges for model accuracy and training efficiency. This project, completed in Summer 2024 for _CS 7641: Machine Learning_ at Georgia Tech, explores the application of unsupervised learning techniques to group data points and reduce dimensionality, ultimately using these techniques as feature engineering tools to boost supervised neural network performance.

We benchmarked these methods across two distinct domains:

1. **Stock Market Prediction (SP)**: Volatile, continuous technical indicators (e.g., MACD, Bollinger Bands, RSI) for JPM stock from 2009 to 2021.
2. **Tennis Men's Sport (TLS)**: Structured, discrete categorical data representing match format, player height, age, Elo rating, and court win percentages.

---

## 1. Clustering Benchmarks: K-Means vs. Expectation Maximization

We analyzed two primary clustering methods: **K-Means (KM)** (partition-based) and **Expectation Maximization (EM)** (probabilistic Gaussian Mixture Model).

### Expectation Maximization (EM)

- **Stock Market Dataset**: EM excelled when configured with a `full` covariance matrix and `kmeans` initialization. It achieved its highest silhouette score at $K=6$, showing that a probabilistic mixture model can effectively capture the overlapping, noisy, and non-spherical distributions of financial technical indicators.
- **Tennis Dataset**: EM struggled significantly, yielding low or negative silhouette scores. The highly categorical and structured nature of the tennis data did not align with GMM's normal distribution assumptions.

### K-Means (KM)

- For both datasets, K-Means utilizing `k-means++` initialization consistently outperformed random initialization, leading to lower inertia and faster convergence.
- The optimal number of clusters (determined by silhouette analysis and elbow method) was **$K=5$ to $7$** for the stock market dataset, and **$K=6$ to $8$** for the tennis dataset.

<pre><code class="language-plotly">
{
  "data": [
    {
      "x": [1.2, 1.5, 1.8, 2.1, 1.4, 1.6, 2.0, 1.7, 1.9, 1.3],
      "y": [2.5, 3.1, 2.8, 3.5, 2.9, 3.0, 3.4, 3.2, 2.7, 3.3],
      "mode": "markers",
      "type": "scatter",
      "name": "Cluster 1: High Growth",
      "marker": { "size": 10, "color": "#0050c0" }
    },
    {
      "x": [-1.5, -1.2, -1.8, -1.0, -1.4, -1.6, -1.1, -1.3, -1.7, -1.9],
      "y": [-0.5, -0.8, -0.2, -0.6, -0.4, -0.7, -0.3, -0.5, -0.9, -0.1],
      "mode": "markers",
      "type": "scatter",
      "name": "Cluster 2: Defensive",
      "marker": { "size": 10, "color": "#0f9d58" }
    },
    {
      "x": [0.1, 0.5, -0.2, 0.3, -0.5, 0.2, -0.1, 0.4, 0.0, -0.3],
      "y": [1.1, 1.5, 0.8, 1.2, 0.9, 1.4, 1.0, 1.3, 0.7, 1.2],
      "mode": "markers",
      "type": "scatter",
      "name": "Cluster 3: Moderate Yield",
      "marker": { "size": 10, "color": "#ff6f00" }
    },
    {
      "x": [1.65, -1.45, 0.09],
      "y": [3.07, -0.5, 1.11],
      "mode": "markers",
      "type": "scatter",
      "name": "Cluster Centroids",
      "marker": { "size": 15, "symbol": "x", "color": "#8e24aa", "line": { "width": 2 } }
    }
  ],
  "layout": {
    "title": "K-Means Clustering Analysis of Financial Assets (PCA)",
    "xaxis": { "title": "Principal Component 1" },
    "yaxis": { "title": "Principal Component 2" }
  }
}
</code></pre>

GMM/EM is a soft-clustering method that models clusters as probability distributions with flexible covariance shapes (spherical, diagonal, tied, or full), allowing it to fit complex financial data where K-Means (which assumes isotropic spherical clusters) fails to generalize.

---

## 2. Dimensionality Reduction: PCA, ICA, and RP

To combat the "curse of dimensionality," we evaluated three dimensionality reduction algorithms:

- **Principal Component Analysis (PCA)**: Focuses on maximizing variance and preserving global structure. Our explained variance analysis showed that just **6 principal components** were sufficient to capture over **95% of the total variance** in both datasets, demonstrating high information retention.
- **Independent Component Analysis (ICA)**: Focuses on statistical independence and maximizing non-Gaussianity. For the Stock Market dataset, ICA proved highly effective, achieving the lowest reconstruction error. Kurtosis analysis showed statistical independence peaking around **12-14 components** for stocks and **8 components** for tennis.
- **Randomized Projections (RP)**: Guided by the Johnson-Lindenstrauss lemma, RP projects data onto a lower-dimensional space using random matrices. While computationally very cheap, it suffered from higher reconstruction errors and fluctuating downstream performance compared to PCA and ICA.

---

## 3. Downstream Classifier Boost: Neural Network Integration

The ultimate test of our unsupervised pipeline was whether the clustered labels and reduced dimensional features could enhance a Multi-Layer Perceptron (MLP) Neural Network classifier.

We trained the neural network under three conditions:

1. Original high-dimensional feature set.
2. Clustered labels mapped to targets (buy/hold/sell for stocks).
3. Dimensionality-reduced feature spaces.

### Key Findings

- **Feature Generation via Clustering**: Using KMeans cluster centers to map and re-label targets actually outperformed manual feature tuning.
- **Dimensionality Reduction Integration**: Training the Neural Network on PCA and ICA reduced features (e.g., `PCA_KMeans_10`) yielded a massive training speedup.
- **ICA Dominance**: The **ICA + KMeans** pipeline achieved near-perfect training and testing performance on the Stock Market dataset, indicating that extracting independent non-Gaussian components succeeded in filtering out the high-frequency financial market noise that typically leads to neural network overfitting.

---

## Conclusion & Occam's Razor

Unsupervised learning is not merely an exploratory tool. When integrated properly, clustering and dimensionality reduction act as powerful filters for noise. As highlighted in our benchmarking, simpler models like K-Means combined with statistical decomposition (PCA/ICA) provide a robust, computationally efficient foundation that outperforms raw neural network training on noisy datasets.
