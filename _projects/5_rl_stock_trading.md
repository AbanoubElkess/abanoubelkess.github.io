---
layout: page
title: Reinforcement Learning for Stock Trading
description: Deep reinforcement learning models and non-stationary policy optimization engines for automated financial trading.
importance: 5
category: academic
img: /assets/img/stock_trading_thumb.png
---

### Project Overview

Financial asset trading is a highly challenging domain for classical machine learning due to low signal-to-noise ratios and non-stationary market regimes (such as sudden shifts in volatility or macroeconomic trends). Reinforcement learning (RL) agents often suffer from policy collapse when trained on historical data, as standard formulations assume a stationary Markov Decision Process (MDP) that does not hold in real-world trading environments.

This academic research project at Georgia Tech developed a robust deep RL framework that uses adaptive policy exploration and dynamic risk-adjusted reward functions to maintain stable trading performance across shifting market regimes.

---

### MDP & Reward Formulation

We model the portfolio trading process as a discrete-time Markov Decision Process (MDP):

$$\mathcal{M} = (\mathcal{S}, \mathcal{A}, \mathcal{P}, \mathcal{R}, \gamma)$$

#### 1. State Space $\mathcal{S}_t$

The state vector at time $t$ encapsulates local market dynamics and current portfolio state:

$$\mathbf{s}_t = [\mathbf{p}_t, \mathbf{v}_t, \mathbf{f}_t, \mathbf{w}_t, c_t]$$

where:

- $\mathbf{p}_t \in \mathbb{R}^K$ represents the closing prices of the $K$ assets.
- $\mathbf{v}_t \in \mathbb{R}^K$ represents the rolling price variances.
- $\mathbf{f}_t$ represents technical indicators (such as MACD, RSI, and Bollinger Bands).
- $\mathbf{w}_t \in [0, 1]^K$ represents the current portfolio asset allocation weights.
- $c_t$ is the liquid cash balance.

#### 2. Action Space $\mathcal{A}_t$

The action vector $\mathbf{a}_t \in [-1, 1]^K$ represents continuous target allocation adjustments, where positive values denote buying, negative values denote selling, and zero denotes holding.

#### 3. Risk-Adjusted Reward Function $\mathcal{R}_t$

Optimizing for absolute return often results in agents taking high-risk positions. To enforce risk management, we formulate the reward based on the rolling Sharpe Ratio of the portfolio return $R_p$:

$$\mathcal{R}_t = \frac{\mathbb{E}\left[ R_p - R_f \right]}{\sigma(R_p)}$$

where $R_f$ is the risk-free rate and $\sigma(R_p)$ is the standard deviation of portfolio returns over a rolling 30-day window.

---

### Policy Optimization with Non-Stationary Adaptation

We implemented a custom Actor-Critic model based on Proximal Policy Optimization (PPO). To prevent the policy from converging prematurely during stable markets and failing during sudden regime changes, we introduced adaptive entropy regularization.

```
       Current Market State (s_t) ──► [ Actor Network ] ──► Continuous Action (a_t)
                                           │
                                           ▼ (PPO Clip Loss)
  [ Policy Entropy H ] ◄─────────── [ Loss Function ] ◄─── [ Critic Advantage A_t ]
            │
            ▼ (Multiplied by Volatility-Scaled Beta)
    Entropy Regularized Update
```

The objective function maximizes:

$$\mathcal{L}_{\text{CLIP}}(\theta) = \hat{\mathbb{E}}_t \left[ \min\left( r_t(\theta)\hat{A}_t, \text{clip}\left(r_t(\theta), 1-\epsilon, 1+\epsilon\right)\hat{A}_t \right) \right] + \beta(v_t) \mathcal{H}\left(\pi_{\theta}(\cdot | \mathbf{s}_t)\right)$$

where:

- $r_t(\theta) = \frac{\pi_{\theta}(a_t|s_t)}{\pi_{\theta_{\text{old}}}(a_t|s_t)}$ is the probability ratio.
- $\hat{A}_t$ is the generalized advantage estimator computed by the Critic network.
- $\epsilon$ is the clipping hyperparameter ($0.2$).
- $\mathcal{H}$ is the policy entropy, which measures exploration diversity.
- $\beta(v_t)$ is a scaling factor that dynamically increases entropy regularization when market volatility $v_t$ rises, forcing the agent to explore safer hedging strategies during high-risk regimes.

---

### Key Outcomes & Technical Impact

- **Risk-Adjusted Performance**: Achieved a **$35\%$** higher Sharpe Ratio in backtesting compared to standard Deep Q-Network (DQN) baselines and a simple buy-and-hold index strategy.
- **Drawdown Mitigation**: Reduced maximum portfolio drawdown by **$18\%$** during simulated market shocks (such as historical high-volatility events) through the action of the dynamic volatility-scaled entropy constraint.
- **Slippage Modeling**: Built a high-fidelity backtesting simulator incorporating realistic transaction costs ($0.1\%$ per trade), order latency, and bid-ask spreads, ensuring the model's simulated returns transfer effectively to live trading conditions.
