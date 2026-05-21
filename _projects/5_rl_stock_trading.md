---
layout: page
title: Reinforcement Learning for Stock Trading
description: Deep reinforcement learning models and non-stationary policy optimization engines for automated financial trading.
importance: 5
category: academic
area: "Machine Learning & Data Science"
img: /assets/img/stock_trading_thumb.png
toc:
  sidebar: left
---

### Project Overview

Financial markets represent a highly challenging domain for classical machine learning due to low signal-to-noise ratios, non-stationarity, and regime-dependent dynamics (e.g., shifts in volatility, macroeconomic conditions, or monetary policy). Reinforcement learning (RL) agents often suffer from policy collapse or severe overfitting when trained on historical data, as standard formulations assume a stationary Markov Decision Process (MDP).

This project developed a robust, production-grade deep reinforcement learning framework that implements adaptive policy exploration and dynamic, risk-adjusted reward functions to maintain stable trading performance across shifting market regimes. By incorporating a high-fidelity transaction cost simulator and non-stationary policy regularization, the system achieves consistent risk-adjusted returns while mitigating extreme drawdowns.

---

### Markov Decision Process Formulation

The portfolio trading task is formulated as a discrete-time Markov Decision Process (MDP), defined by the tuple $\mathcal{M} = (\mathcal{S}, \mathcal{A}, \mathcal{P}, \mathcal{R}, \gamma)$, where $\mathcal{S}$ is the state space, $\mathcal{A}$ is the action space, $\mathcal{P}$ is the transition probability distribution, $\mathcal{R}$ is the reward function, and $\gamma \in (0, 1)$ is the temporal discount factor.

#### 1. State Representation $\mathbf{s}_t$

The state vector at time step $t$ encodes both local market features and the current internal portfolio status to ensure the Markov property holds:

$$\mathbf{s}_t = [\mathbf{p}_t, \mathbf{v}_t, \mathbf{f}_t, \mathbf{w}_{t-1}, c_t]$$

where:

- $\mathbf{p}_t \in \mathbb{R}^D$ represents the normalized closing prices of the $D$ assets.
- $\mathbf{v}_t \in \mathbb{R}^D$ represents the rolling price variances over multiple lookback windows (e.g., 5-day, 20-day, and 60-day).
- $\mathbf{f}_t \in \mathbb{R}^F$ is a set of technical and statistical indicators, including:
  - **Relative Strength Index (RSI)**: Measures momentum over a 14-day window.
  - **Moving Average Convergence Divergence (MACD)**: Captures trend-following signals.
  - **Bollinger Bands**: Represents local volatility boundaries.
  - **Autoregressive coefficients**: Captures local time-series dependencies.
- $\mathbf{w}_{t-1} \in [0, 1]^D$ represents the portfolio allocation weights from the previous step, satisfying $\sum_{i=1}^D w_{t-1, i} \le 1$.
- $c_t \in [0, 1]$ is the normalized liquid cash proportion of the portfolio.

#### 2. Action Space $\mathcal{A}$

To allow the agent to optimize asset allocations smoothly, the action space is defined as a continuous vector $\mathbf{a}_t \in [-1, 1]^D$.

The actor network outputs raw allocation changes, which are processed through a portfolio manager layer:

- Positive values represent buying or increasing exposure to asset $i$.
- Negative values represent selling or reducing exposure.
- Zero represents holding the current position.

The target allocation weights $\mathbf{w}_t$ are calculated as:

$$\mathbf{w}_{t} = \text{Softmax}(\mathbf{w}_{t-1} + \mathbf{a}_t)$$

This formulation enforces the self-financing constraint $\sum_{i=1}^D w_{t, i} = 1$ and prevents short-selling (allocations are constrained to non-negative values).

#### 3. Risk-Adjusted Reward Function $\mathcal{R}_t$

Optimizing purely for absolute returns leads to volatile policies that take excessive risks. To enforce risk management, we define the reward function based on a localized, rolling Sharpe Ratio combined with transaction cost penalties:

$$\mathcal{R}_t = \frac{\mathbb{E}\left[ R_{p, t} - R_f \right]}{\sigma(R_{p, t})} - \lambda_{\text{cost}} \sum_{i=1}^D |w_{t, i} - w'_{t, i}|$$

where:

- $R_{p, t}$ is the portfolio return at time step $t$.
- $R_f$ is the risk-free rate (assumed constant or fetched dynamically).
- $\sigma(R_{p, t})$ is the standard deviation of portfolio returns calculated over a rolling 30-day window.
- $w'_{t, i}$ represents the adjusted weight of asset $i$ just before time step $t$ due to price movements:

  $$w'_{t, i} = \frac{w_{t-1, i} (1 + R_{i, t})}{1 + R_{p, t}}$$

- $\lambda_{\text{cost}}$ is a penalty coefficient scaling the impact of transaction costs (commission and slippage).

---

### Actor-Critic Architecture & Training Infrastructure

We implemented a custom Actor-Critic model optimized for non-stationary environments, utilizing Proximal Policy Optimization (PPO) as the core optimization algorithm.

```
       ┌───────────────────────────────┐
       │   State Input s_t (RSI, Vol)  │
       └───────────────────────────────┘
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
     ┌──────────────┐     ┌──────────────┐
     │ LSTM Encoder │     │ LSTM Encoder │
     └──────────────┘     └──────────────┘
             │                   │
             ▼                   ▼
     ┌──────────────┐     ┌──────────────┐
     │  Actor Head  │     │ Critic Head  │
     │  (Policy)    │     │ (Value Fn)   │
     └──────────────┘     └──────────────┘
             │                   │
             ▼                   ▼
       Action a_t           Value V(s_t)
```

#### 1. Temporal Feature Extraction

To process sequential dependencies in financial data, the policy and value networks share a temporal feature extractor:

- **Bi-directional LSTM layer**: Captures short- and medium-term temporal dependencies.
- **Attention layer**: Applies temporal attention over a 30-day lookback window, highlighting historical regime shifts.

#### 2. Regime-Aware Exploration Regularization

In financial markets, high-volatility regimes require the agent to explore safer hedging strategies, whereas low-volatility regimes permit exploitation of stable trends. We introduced dynamic entropy regularization scaled by market volatility:

$$\mathcal{L}_{\text{entropy}}(\theta) = \beta(v_t) \mathcal{H}\left(\pi_{\theta}(\cdot | \mathbf{s}_t)\right)$$

The dynamic scaling coefficient $\beta(v_t)$ is formulated as:

$$\beta(v_t) = \beta_0 \cdot \left( 1 + \tanh\left( \frac{v_t - \bar{v}}{\sigma_v} \right) \right)$$

where:

- $v_t$ is the current rolling volatility of the market index.
- $\bar{v}$ and $\sigma_v$ are the historical mean and standard deviation of market volatility, respectively.
- $\beta_0$ is the baseline entropy regularization coefficient.
- Under high market stress ($v_t \gg \bar{v}$), $\beta(v_t)$ increases, prompting the agent to maintain high policy entropy $\mathcal{H}$, which prevents premature convergence and encourages robust exploration.

#### 3. Proximal Policy Optimization (PPO) Clip Loss

The policy parameter updates are bounded using the clipped surrogate objective to ensure stable policy updates:

$$\mathcal{L}_{\text{CLIP}}(\theta) = \hat{\mathbb{E}}_t \left[ \min\left( r_t(\theta)\hat{A}_t, \text{clip}\left(r_t(\theta), 1-\epsilon, 1+\epsilon\right)\hat{A}_t \right) \right]$$

where:

- $r_t(\theta) = \frac{\pi_{\theta}(a_t|\mathbf{s}_t)}{\pi_{\theta_{\text{old}}}(a_t|\mathbf{s}_t)}$ is the probability ratio.
- $\hat{A}_t$ is the generalized advantage estimator (GAE) computed by the Critic network:

  $$\hat{A}_t = \sum_{l=0}^{\infty} (\gamma \lambda)^l \delta_{t+l}^V$$

  with $\delta_t^V = R_t + \gamma V_{\phi}(\mathbf{s}_{t+1}) - V_{\phi}(\mathbf{s}_t)$.

---

### Simulator and Slippage Modeling

Deploying RL models directly from idealized simulations to live markets often fails due to execution slippage and friction. We built a high-fidelity simulator to bridge this gap.

#### 1. Frictional Impact Model

The simulator models transaction friction using a two-tier cost function:

$$\text{Cost}(\Delta w) = \text{Commission} + \text{Slippage}$$

- **Commission**: Fixed at $0.05\%$ of the transaction volume.
- **Slippage**: Modeled as a quadratic function of the trade size relative to the average daily volume (ADV) of the asset:

  $$\text{Slippage}_i = \eta \left( \frac{\Delta V_i}{\text{ADV}_i} \right)^2$$

  where $\Delta V_i$ is the volume traded and $\eta$ is a market impact coefficient.

#### 2. Robust Validation Strategy

To prevent overfitting to specific historical regimes, we designed a rigorous evaluation pipeline:

- **Walk-Forward Validation**: The model is trained on a rolling window of 3 years, validated on the subsequent 6 months, and tested on the following 6 months, stepping forward iteratively.
- **Regime-Specific Stress Testing**: We evaluated the policy on historical high-stress periods, including the 2008 financial crisis and the 2020 market crash, to test drawdown mitigation.

---

### Experimental Results & Performance Benchmarks

The model was evaluated using historical data of a diversified basket of 20 liquid equities spanning the period from 2015 to 2023.

#### 1. Performance Metrics

The table below compares the performance of the proposed regime-aware PPO agent against standard baselines:

| Metric                    | Buy & Hold | Standard PPO | Regime-Aware PPO (Ours) |
| :------------------------ | :--------: | :----------: | :---------------------: |
| **Annualized Return**     |   10.4%    |    14.2%     |        **18.7%**        |
| **Annualized Volatility** |   16.2%    |    13.8%     |        **11.5%**        |
| **Sharpe Ratio**          |    0.64    |     1.03     |        **1.63**         |
| **Sortino Ratio**         |    0.88    |     1.41     |        **2.24**         |
| **Max Drawdown**          |   -32.4%   |    -21.1%    |       **-12.8%**        |
| **Calmar Ratio**          |    0.32    |     0.67     |        **1.46**         |

#### 2. Policy Robustness Analysis

- **Drawdown Mitigation**: During simulated market shocks, the dynamic volatility-scaled entropy constraint successfully forced the agent to reallocate capital into liquid cash and low-beta assets, reducing the maximum drawdown by $18\%$ compared to standard PPO.
- **Slippage Robustness**: Under high friction ($\lambda_{\text{cost}} > 0.002$), the agent learned to reduce trading frequency, avoiding unprofitable short-term trades and focusing on medium-term macroeconomic trends.
