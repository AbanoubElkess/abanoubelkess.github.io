---
layout: post
title: "Heuristic Optimization: Analyzing RHC, Simulated Annealing, and Genetic Algorithms"
date: 2024-07-10
categories: machine-learning
description: "A comparative study of randomized optimization heuristics across binary, combinatorial, and neural network weight space problems."
related_posts: false
toc:
  beginning: true
---

Deterministic optimization methods, such as gradient descent, form the backbone of modern machine learning. However, when faced with non-convex, non-smooth, or highly restricted search spaces, deterministic algorithms can easily get trapped in local optima. This project, completed in Summer 2024 for _CS 7641: Machine Learning_ at Georgia Tech, investigates the performance of four Randomized Optimization (RO) heuristics: **Randomized Hill Climbing (RHC)**, **Simulated Annealing (SA)**, **Genetic Algorithms (GA)**, and **Mutual Information Maximizing Input Clustering (MIMIC)**.

We benchmarked these algorithms across three distinct optimization landscapes:

1. **The Flip Flop Problem (FFP)**: A binary optimization challenge where the objective is to maximize transitions between adjacent bits (e.g., '01' or '10') in strings of length $N = 40, 100, 500$.
2. **The N-Queens Problem (NQP)**: A combinatorial constraint satisfaction problem requiring the placement of $N$ queens on an $N \times N$ chessboard without conflicts ($N = 20, 50, 100$).
3. **Neural Network Weight Optimization (SP-NN)**: Optimizing the weights of a Multi-Layer Perceptron (MLP) neural network for stock market prediction on JPM stock data, comparing RO techniques against backpropagation (gradient descent).

All algorithms were implemented using the `mlrose-hiive` Python library.

> The full write-up, including the hyperparameter sweep ranges and the complete
> results table, lives on the project page:
> [Randomized Optimization & Clustering Benchmarks]({{ '/projects/11_randomized_optimization/' | relative_url }}).

---

## 1. The Optimization Algorithms: Strengths and Weaknesses

### Randomized Hill Climbing (RHC)

RHC starts with a random candidate solution and iteratively makes small local adjustments, accepting only changes that improve fitness. To prevent trapping in local optima, we introduced random restarts. This makes RHC fast and efficient on smooth, unimodal landscapes, but it scales poorly in the high-dimensional, rugged spaces where local search traps are dense, N-Queens being the clearest example here.

### Simulated Annealing (SA)

SA introduces a temperature parameter that starts high (allowing the algorithm to probabilistically accept worse candidate solutions) and cools gradually over time. This probabilistic acceptance is what lets SA climb back out of local minima, giving robust performance on both Flip Flop and N-Queens, though the results depend heavily on the cooling schedule chosen (e.g., `GeomDecay`).

### Genetic Algorithms (GA)

GA simulates natural selection by maintaining a population of candidate solutions that evolve over generations through crossover and mutation. This population-based search explores globally rather than locally, and it reached the highest final fitness on both the Flip Flop and N-Queens benchmarks. Maintaining and evaluating whole populations is the cost, making GA by far the most expensive of the four per iteration.

### MIMIC (Mutual Information Maximizing Input Clustering)

MIMIC replaces crossover and mutation by constructing a probabilistic model of the search space, capturing dependencies between variables to generate high-fitness samples. This dependency modeling is what makes it effective in binary spaces (Flip Flop) and structured constraint spaces (N-Queens), while the cost of updating the distribution grows rapidly with the number of variables.

<div class="row justify-content-sm-center">
  <div class="col-sm-11 mt-3 mt-md-0">
    {% include figure.liquid loading="lazy" path="assets/img/figures/ro_converged_fitness.svg" alt="Grouped bar chart of converged mean fitness for three randomized optimization algorithms at each problem size. The genetic algorithm leads on both problems, and its margin widens as the N-Queens board size grows." title="Converged mean fitness by algorithm and problem size" class="img-fluid" zoomable=true caption="Converged mean fitness for each algorithm at each problem size, as stated in the project report. GA leads on both problems and its margin widens sharply with board size on N-Queens." %}
  </div>
</div>

---

## 2. Benchmark Results and Convergence Profiles

### Flip Flop and N-Queens Convergence

- For **Flip Flop**, both GA and MIMIC rapidly converged to optimal fitness, while RHC and SA required more iterations and showed higher variance as string length $N$ grew to $500$.
- For **N-Queens**, SA and GA outperformed RHC. The strict diagonal and row/column constraints of NQP create a highly rugged fitness landscape where RHC gets trapped. SA escapes it through probabilistic acceptance and GA through crossover diversity, both of which find conflict-free placements that pure hill climbing cannot reach.

### Neural Network Weight Optimization

We trained an MLP classifier using RHC, SA, and GA to optimize its weights directly, benchmarking them against standard Gradient Descent (GD) with backpropagation.

- **Gradient Descent** achieved the best overall accuracy and generalization, leveraging exact gradient information.
- Among the RO methods, **Simulated Annealing** performed best, presenting a robust alternative in complex, volatile environments where gradient calculations might be noisy or unavailable.
- **Genetic Algorithms** struggled in neural network training due to the high-dimensional weight space, which caused massive population evaluation overhead (wall-clock times exceeding 4,000 seconds).

While GA converges to superior global optima, the computational overhead of crossover, mutation, and population fitness evaluations means it can be orders of magnitude slower in wall-clock time than local search strategies like RHC or SA.

---

## 3. Key Takeaways & Guidelines

When selecting an optimization algorithm, consider the structure of the landscape:

1. **For simple or smooth landscapes**: Use **RHC** with multiple random restarts for maximum speed.
2. **For highly rugged landscapes with local traps**: Use **Simulated Annealing** with a geometric cooling schedule to allow exploration.
3. **For complex constraint-satisfaction tasks**: Use **Genetic Algorithms** or **MIMIC** if computational budget permits, as their global search characteristics are highly effective at finding global optima.
