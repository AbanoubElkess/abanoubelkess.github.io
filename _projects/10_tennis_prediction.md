---
layout: page
title: Tennis Match Winner Predictions
description: Predictive modeling framework for professional tennis matches using surface-specific Elo ratings, time-decay factors, Platt calibration, and Gradient Boosting machines.
importance: 10
category: academic
area: "Machine Learning & Data Science"
img: /assets/img/tennis_dashboard.png
toc:
  sidebar: left
---

### Project Overview

Predicting the outcome of professional tennis matches is a complex task due to the influence of surface types (hard, clay, and grass), recent player form, head-to-head dynamics, and physical recovery times. This project implements a predictive pipeline designed to estimate match-winner probabilities for ATP and WTA matches. The architecture combines custom mathematical feature-engineering pipelines with Gradient Boosting Decision Trees (GBDTs), calibrated using Platt scaling to output reliable, probabilistic predictions.

---

### Feature Engineering & Mathematical Modeling

The pipeline constructs historical and tournament-specific features to capture various dimensions of player capability and match context.

#### 1. Surface-Specific Elo Ratings

Standard Elo models treat all matches identically, ignoring the substantial performance disparities players exhibit on different court surfaces. We formulate a multi-dimensional Elo system where each player has a general Elo rating $R_{\text{gen}}$ and three surface-specific ratings $R_{\text{hard}}$, $R_{\text{clay}}$, and $R_{\text{grass}}$.

The expected probability of player $A$ defeating player $B$ is given by:

$$E_A = \frac{1}{1 + 10^{(R_B - R_A)/400}}$$

Upon completion of a match, the rating update is computed as:

$$R'_A = R_A + K \cdot (S_A - E_A)$$

where $S_A \in \{0, 1\}$ is the actual outcome (1 for a win, 0 for a loss), and $K$ is the update weight factor. The $K$-factor is dynamically scaled based on the match format (e.g., higher weight for Grand Slams compared to ATP 250 events) and the player's total match count to ensure faster convergence for newcomers:

$$K = \frac{K_{\text{base}}}{(N_{\text{matches}} + 1)^{\gamma}}$$

#### 2. Time-Decay Adjustments

To account for injury layoffs and aging, ratings are adjusted using an exponential time-decay function. If a player has been inactive for a duration of $\Delta t$ days, their rating decays toward the population mean $R_{\text{mean}}$:

$$R_{\text{decayed}} = R_{\text{last}} \cdot e^{-\alpha \Delta t} + R_{\text{mean}} \cdot (1 - e^{-\alpha \Delta t})$$

where $\alpha$ is a hyperparameter determining the rate of rating decay.

---

### Model Architecture & Loss Function

The predictive core utilizes a Gradient Boosting Machine (LightGBM) to handle non-linear feature interactions and missing data elements.

#### 1. Optimization Objective

The classifier is trained to minimize the Binary Cross-Entropy (Log-Loss) of the predicted probabilities, ensuring that the model penalizes overconfident incorrect predictions:

$$\mathcal{L} = -\frac{1}{N} \sum_{i=1}^{N} \left[ y_i \log(p_i) + (1 - y_i) \log(1 - p_i) \right]$$

where $y_i \in \{0, 1\}$ is the true label (win/loss of player $A$), and $p_i$ is the predicted probability.

#### 2. Platt Scaling Calibration

Since decision tree ensembles do not naturally output calibrated probabilities, we apply Platt scaling to map the raw margin outputs $f(x)$ of the gradient boosted model to well-calibrated probabilities. We fit a sigmoid function over the validation predictions:

$$P(y = 1 \mid f(x)) = \frac{1}{1 + e^{A f(x) + B}}$$

The parameters $A$ and $B$ are determined by minimizing the negative log-likelihood of the calibration dataset.

---

### Implementation & Results

The system achieves competitive predictive performance, outperforming baseline bookmaker odds on several validation subsets. A summary of the model performance across different surfaces is detailed below:

| Model / Surface      | Hard Court Accuracy | Clay Court Accuracy | Grass Court Accuracy |   Overall Log-Loss   |
| :------------------- | :-----------------: | :-----------------: | :------------------: | :------------------: |
| Baseline Elo         |        66.8%        |        65.2%        |        64.9%         |        0.612         |
| Optimized GBDT (Raw) |        68.9%        |        67.5%        |        66.8%         | 0.589 (Uncalibrated) |
| Calibrated GBDT      |        69.4%        |        68.1%        |        67.3%         |        0.565         |

---

### Reference Material & PDF Download

For a comprehensive review of the statistical methodologies, feature correlations, and detailed experimental setups, you can download the full project report:

- [Tennis Match Predictions Project Report](/assets/pdf/TennisMatchPrediction_Project.pdf)
