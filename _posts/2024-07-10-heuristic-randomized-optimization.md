---
layout: post
title: "Heuristic Optimization: Analyzing RHC, Simulated Annealing, and Genetic Algorithms"
date: 2024-07-10
categories: machine-learning
description: "A comparative study of randomized optimization heuristics across binary, combinatorial, and neural network weight space problems."
related_posts: false
chart:
  plotly: true
---

Deterministic optimization methods, such as gradient descent, form the backbone of modern machine learning. However, when faced with non-convex, non-smooth, or highly restricted search spaces, deterministic algorithms can easily get trapped in local optima. This project, completed in Summer 2024 for _CS 7641: Machine Learning_ at Georgia Tech, investigates the performance of four Randomized Optimization (RO) heuristics: **Randomized Hill Climbing (RHC)**, **Simulated Annealing (SA)**, **Genetic Algorithms (GA)**, and **Mutual Information Maximizing Input Clustering (MIMIC)**.

We benchmarked these algorithms across three distinct optimization landscapes:

1. **The Flip Flop Problem (FFP)**: A binary optimization challenge where the objective is to maximize transitions between adjacent bits (e.g., '01' or '10') in strings of length $N = 40, 100, 500$.
2. **The N-Queens Problem (NQP)**: A combinatorial constraint satisfaction problem requiring the placement of $N$ queens on an $N \times N$ chessboard without conflicts ($N = 20, 50, 100$).
3. **Neural Network Weight Optimization (SP-NN)**: Optimizing the weights of a Multi-Layer Perceptron (MLP) neural network for stock market prediction on JPM stock data, comparing RO techniques against backpropagation (gradient descent).

All algorithms were implemented using the `mlrose-hiive` Python library.

---

## 1. The Optimization Algorithms: Strengths and Weaknesses

### Randomized Hill Climbing (RHC)

RHC starts with a random candidate solution and iteratively makes small local adjustments, accepting only changes that improve fitness. To prevent trapping in local optima, we introduced random restarts.

- **Verdict**: Highly efficient and fast for simple, smooth, unimodal landscapes. However, it scales poorly in high-dimensional, rugged spaces (like N-Queens) where local search traps are dense.

### Simulated Annealing (SA)

SA introduces a temperature parameter that starts high—allowing the algorithm to probabilistically accept worse candidate solutions—and gradually cools down over time.

- **Verdict**: The probabilistic acceptance allows SA to escape local minima. Its performance is highly robust across both Flip Flop and N-Queens, though it is highly sensitive to the chosen cooling schedule (e.g., `GeomDecay`).

### Genetic Algorithms (GA)

GA simulates natural selection by maintaining a population of candidate solutions that evolve over generations through crossover and mutation.

- **Verdict**: Outstanding global exploration. GA consistently achieved the highest final fitness scores in both the Flip Flop and N-Queens benchmarks. However, maintaining and evaluating populations is extremely computationally expensive.

### MIMIC (Mutual Information Maximizing Input Clustering)

MIMIC replaces crossover/mutation by constructing a probabilistic model of the search space, capturing dependencies between variables to generate high-fitness samples.

- **Verdict**: Exceptionally effective in binary spaces (Flip Flop) and structured constraint spaces (N-Queens). However, the cost of updating the probability distribution scales rapidly with the number of variables.

---

## 2. Benchmark Results and Convergence Profiles

### Flip Flop and N-Queens Convergence

- For **Flip Flop**, both GA and MIMIC rapidly converged to optimal fitness, while RHC and SA required more iterations and showed higher variance as string length $N$ grew to $500$.
- For **N-Queens**, SA and GA outperformed RHC. The strict diagonal and row/column constraints of NQP create a highly rugged fitness landscape where RHC gets trapped, whereas SA utilizes its thermal energy and GA utilizes its crossover diversity to find conflict-free placements.

### Neural Network Weight Optimization

We trained an MLP classifier using RHC, SA, and GA to optimize its weights directly, benchmarking them against standard Gradient Descent (GD) with backpropagation.

- **Gradient Descent** achieved the best overall accuracy and generalization, leveraging exact gradient information.
- Among the RO methods, **Simulated Annealing** performed best, presenting a robust alternative in complex, volatile environments where gradient calculations might be noisy or unavailable.
- **Genetic Algorithms** struggled in neural network training due to the high-dimensional weight space, which caused massive population evaluation overhead (wall-clock times exceeding 4,000 seconds).

<pre><code class="language-plotly">
{
  "data": [
    {
      "x": [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000],
      "y": [10, 35, 55, 68, 76, 82, 85, 88, 90, 92, 93, 94, 95, 96, 96.5, 97, 97.2, 97.5, 97.8, 98, 98.2],
      "mode": "lines+markers",
      "type": "scatter",
      "name": "Genetic Algorithm (GA)",
      "line": { "color": "#8e24aa", "width": 3 }
    },
    {
      "x": [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000],
      "y": [10, 28, 42, 38, 55, 62, 59, 70, 78, 83, 85, 87, 88.5, 89.2, 89.8, 90.1, 90.3, 90.5, 90.6, 90.8, 90.9],
      "mode": "lines+markers",
      "type": "scatter",
      "name": "Simulated Annealing (SA)",
      "line": { "color": "#ff6f00", "width": 2.5 }
    },
    {
      "x": [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000],
      "y": [10, 45, 52, 52, 52, 52.5, 52.5, 52.5, 52.5, 52.5, 52.5, 52.5, 52.5, 52.5, 52.5, 52.5, 52.5, 52.5, 52.5, 52.5, 52.5],
      "mode": "lines+markers",
      "type": "scatter",
      "name": "Randomized Hill Climbing (RHC)",
      "line": { "dash": "dash", "color": "#0050c0", "width": 2 }
    },
    {
      "x": [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000],
      "y": [10, 50, 72, 83, 89, 91, 92, 92.5, 92.8, 93, 93.2, 93.3, 93.4, 93.5, 93.6, 93.6, 93.7, 93.7, 93.8, 93.8, 93.8],
      "mode": "lines+markers",
      "type": "scatter",
      "name": "MIMIC",
      "line": { "color": "#0f9d58", "width": 2.5 }
    }
  ],
  "layout": {
    "title": "Heuristic Optimization Algorithm Convergence (N-Queens)",
    "xaxis": { "title": "Iterations / Generations" },
    "yaxis": { "title": "Best Fitness Score" }
  }
}
</code></pre>

> [!WARNING]
> While GA converges to superior global optima, the computational overhead of crossover, mutation, and population fitness evaluations means it can be orders of magnitude slower in wall-clock time than local search strategies like RHC or SA.

---

## 3. Key Takeaways & Guidelines

When selecting an optimization algorithm, consider the structure of the landscape:

1. **For simple or smooth landscapes**: Use **RHC** with multiple random restarts for maximum speed.
2. **For highly rugged landscapes with local traps**: Use **Simulated Annealing** with a geometric cooling schedule to allow exploration.
3. **For complex constraint-satisfaction tasks**: Use **Genetic Algorithms** or **MIMIC** if computational budget permits, as their global search characteristics are highly effective at finding global optima.
