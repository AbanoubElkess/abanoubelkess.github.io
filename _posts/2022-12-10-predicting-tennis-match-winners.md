---
layout: post
title: "Predicting Professional Tennis Match Winners using Gradient Boosting"
date: 2022-12-10
categories: machine-learning
description: "How we engineered a robust data pipeline and compared classifier ensembles to predict ATP tennis match outcomes with over 80% accuracy."
related_posts: false
chart:
  plotly: true
---

In professional sports, tennis stands out as a unique 1v1 contest with no fixed time limit. While sports like soccer and baseball have seen massive revolutions in data analytics, tennis analytics remains in a relatively early stage. This project, completed as part of the _CSE 6242: Data and Visual Analytics_ course at Georgia Tech in Fall 2022, addresses this opportunity by building an end-to-end machine learning system and an interactive web dashboard to predict professional men's tennis match winners.

## The Data Pipeline & Preprocessing Challenge

Our primary data source was Jeff Sackman's comprehensive ATP tennis match database. Initially, the database contained **182,964 historical matches**. However, to build a reliable predictive model, we had to perform extensive data cleaning and filtering:

1. **Active Players Filter**: We restricted our predictions to matches where both players were active, ensuring our model is relevant to current tour matches.
2. **Missing Feature Cleanup**: Matches lacking critical player attributes or match characteristics were pruned.
3. **Player Order Bias Mitigation**: The raw database stores match records from the perspective of "winner" and "loser". Feeding this directly into a model would lead to trivial classification or severe ordering bias. To resolve this, we randomly scrambled winners and losers into `Player 1` and `Player 2` and recalculated statistical attributes to ensure the model remains completely order-agnostic.

After filtering, our final calibration and testing dataset consisted of **16,049 clean data points**.

## Feature Engineering

Through domain knowledge and literature survey, we selected **12 core features** divided into four main categories:

- **Match-based features**: Court surface (clay, grass, hard), match format (best of 3 vs. best of 5), and environment (indoor vs. outdoor).
- **Player characteristics**: Player height, age, and backhand style (one-handed vs. two-handed).
- **Current rankings**: Official ATP rankings and computed Elo ratings.
- **Historical performance**: Player win percentage (general win %, win % under the same match format, and win % on the same court surface).

We compared three feature sets to analyze the curse of dimensionality. **Feature Set 1** (including backhand style, height, surface-specific win %, and indoor/outdoor win %) provided the best balance of model complexity and generalization.

## Machine Learning Benchmarks

We approached the prediction as a binary classification problem. Using an $80\%/20\%$ train/test split, we trained and tuned five classification algorithms using grid search and 10-fold cross-validation. We evaluated the models using the F1-score to balance precision and recall:

| ML Model                 | Train F1 Score  | Test F1 Score |
| :----------------------- | :-------------: | :-----------: |
| **Gradient Boosting**    |    **0.812**    |   **0.733**   |
| **AdaBoost**             | 1.000 (Overfit) |     0.731     |
| **Neural Network (MLP)** |      0.712      |     0.706     |
| **k-Nearest Neighbors**  |      0.719      |     0.684     |
| **Decision Tree**        |      0.712      |     0.677     |

**Gradient Boosting** emerged as our champion model, demonstrating superior resilience against overfitting while delivering a strong test F1-score.

## The Interactive Dashboard

To make the predictive engine accessible, we built a web application using the **Dash** framework (Python, Plotly.js, and React.js) and hosted it on Render.

The application allows users to select any two active ATP players and customize the match conditions (surface, format, environment). The dashboard then displays:

1. **Predicted Winner**: The predicted winning player and probability.
2. **Player Radar Charts**: A multi-axis comparison of the players' win percentages across different surfaces.
3. **Geographic Choropleth Map**: Visualizing the home countries of the selected players.

<pre><code class="language-plotly">
{
  "data": [
    {
      "type": "scatterpolar",
      "r": [82, 75, 90, 85, 78, 82],
      "theta": ["Hard Court Win %", "Clay Court Win %", "Grass Court Win %", "Elo Percentile", "Service Games Won %", "Hard Court Win %"],
      "fill": "toself",
      "name": "Player A (Novak Djokovic)",
      "line": { "color": "#008080" }
    },
    {
      "type": "scatterpolar",
      "r": [76, 92, 70, 83, 80, 76],
      "theta": ["Hard Court Win %", "Clay Court Win %", "Grass Court Win %", "Elo Percentile", "Service Games Won %", "Hard Court Win %"],
      "fill": "toself",
      "name": "Player B (Rafael Nadal)",
      "line": { "color": "#ff6f00" }
    }
  ],
  "layout": {
    "polar": {
      "radialaxis": {
        "visible": true,
        "range": [0, 100]
      }
    },
    "showlegend": true,
    "title": "Player Performance Radar Comparison"
  }
}
</code></pre>

> [!TIP]
> Mitigating player ordering bias is a crucial step in sports prediction. Scrambling the historical data from winner/loser to Player 1/Player 2 prevents the classifier from learning simple positional patterns instead of actual player attributes.

## Future Extensions

While our model achieves high predictive accuracy, several improvements are planned:

1. **Live-Data Feeds**: Integrating real-time API scoring to update match predictions as play progresses.
2. **Retraining Loop**: Automatically pulling new tournament results to dynamically update player Elo and win percentages.
3. **Betting Market Arbitrage**: Comparing model prediction confidence against bookmaker odds to identify market inefficiencies.
