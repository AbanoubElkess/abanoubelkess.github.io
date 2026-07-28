---
layout: page
title: Tennis Match Winner Predictions
description: Match-winner classifier for men's professional tennis, built on 16,049 filtered matches and 12 engineered features, deployed as an interactive Dash application.
importance: 10
category: academic
area: "Machine Learning & Data Science"
img: /assets/img/figures/tennis_model_f1.svg
toc:
  sidebar: left
---

### Project Overview

Tennis is a one-on-one sport with no clock and decades of consistently recorded match data, which makes it well suited to predictive modeling. Most public analysis stops at isolated statistics, and most prediction sits locked inside betting platforms with no visualization layer. This project set out to combine the two: a classifier that estimates which of two players wins a given match, wrapped in a web application that shows the statistics behind the prediction.

Team project for **CSE6242 Data & Visual Analytics**, Georgia Tech, Fall 2022, with [Sheikh Jalaluddin Mohammad](mailto:jalal@gatech.edu), [Michael S. Rivera](mailto:mrivera63@gatech.edu), and [Mohamad A. Elsayed](mailto:melsayed31@gatech.edu).

---

### Data

Matches were pulled from a PostgreSQL database distributed as a Docker image, giving a starting pool of **182,964 matches**. Two filters were applied: both players must be currently active, and any match missing the required feature values was dropped. That left **16,049 matches** for calibration and testing.

The match database records who won and who lost. Storing the data that way would let a model learn position rather than skill, so winner and loser were scrambled into player 1 and player 2, and the paired statistics were computed symmetrically to keep the model order-agnostic.

Twelve features were selected using entropy and information gain, aided by domain knowledge:

- **Match context** — match format, surface, indoor or outdoor
- **Player attributes** — height, age, one-handed or two-handed backhand
- **Ranking** — official ATP ranking and ELO rating, both taken from the dataset as inputs
- **Win rates** — overall win percentage, and win percentage restricted to the same match format, the same tournament surface, and this format

---

### Models and Evaluation

The problem was treated as binary classification. Five model families were tried, from a plain decision tree up through boosted ensembles, a distance-based method, and a neural network. Data was split 70/30 into training and validation, scaled where the model required it, and each family was tuned by grid search over its own hyperparameters, with validation and learning curves generated to identify overfitting.

**F1 was chosen as the scoring metric** rather than accuracy, since it balances in-sample and out-of-sample behaviour across both classes and is applied identically to the training and test sets.

<div class="row justify-content-sm-center">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/figures/tennis_model_f1.svg" title="Train and test F1 by model family" class="img-fluid" zoomable=true caption="Figure 1: Gradient boosting reaches the highest test F1 at 0.733. AdaBoost fits the training set perfectly (F1 = 1.000) without beating it on test, which is memorization rather than skill. Values transcribed from the project report, Section 5.4." %}
  </div>
</div>

| ML Model            | Train F1  |  Test F1  |
| :------------------ | :-------: | :-------: |
| Decision Tree       |   0.712   |   0.677   |
| Gradient Boosting   | **0.812** | **0.733** |
| Neural Network      |   0.712   |   0.706   |
| Ada Boost           |   1.000   |   0.731   |
| K Nearest Neighbors |   0.719   |   0.684   |

Gradient boosting was selected as the final model. Two results are worth stating plainly rather than glossing over. AdaBoost's perfect training F1 buys it nothing on test, which is exactly the overfitting signature the validation curves were generated to catch. And the neural network, despite the lowest test score of the ensembles, has the narrowest train/test gap of any model tried, at 0.712 against 0.706.

---

### Deployment

The final model was serialized and deployed inside a web application built with **Plotly and Dash**, hosted on Render. A user selects two players and a match context; the application returns the predicted winner alongside the historical statistics that drove the prediction, so the number is never presented without the evidence behind it. Feature datasets were exported to CSV so the application runs without the original PostgreSQL database.

---

### Report

- [Tennis Match Predictions Project Report](/assets/pdf/TennisMatchPrediction_Project.pdf) — full methodology, dataset selection trials, feature engineering, and the learning and validation curves for the final model.
