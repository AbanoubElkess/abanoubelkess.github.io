---
layout: page
title: Domain Specific Language Copilot
description: Generative AI tool that automatically writes Standard Verification Rule Format (SVRF) language code from natural language prompts.
importance: 1
category: work
img: /assets/img/dsl_copilot_thumb.png
related_publications: true
---

### Project Overview

Physical verification rule decks for semiconductor layouts are traditionally written in proprietary Domain-Specific Languages (DSLs), most notably Siemens SVRF (Standard Verification Rule Format). These rule decks specify thousands of geometric, topological, and electrical constraints that a circuit design must satisfy to be manufacturable. Creating and maintaining these decks is a major bottleneck in semiconductor design-technology co-optimization (DTCO).

To address this challenge, we developed a specialized generative AI Copilot. The system translates natural language verification specifications directly into syntactically valid SVRF code blocks, utilizing a closed-loop validation engine to eliminate compiler and linter errors.

---

### Compiler Front-End & LLM Fine-Tuning

The architecture integrates a formal language compiler front-end with an adapted Large Language Model.

#### 1. SVRF Parser and Abstract Syntax Tree (AST) Generation

We constructed a formal grammar for a subset of SVRF using ANTLR. The parser maps layouts and rule definitions to an AST:

$$G = (V, \Sigma, R, S)$$

where:

- $V$ is the set of non-terminal SVRF structures (such as rule blocks or check environments).
- $\Sigma$ is the set of terminal layout operation tokens (such as `EXT`, `INT`, `ENC`, `CONNECT`).
- $R$ represents the production rules mapping statements to structural layout constraints.
- $S$ is the start symbol.

This AST representation allows us to strip comments, normalize variables, and construct semantic representations for code training and validation.

#### 2. Low-Rank Adaptation (LoRA) Fine-Tuning

To specialize the base code model (e.g., StarCoder-15B) on proprietary, sparse SVRF data without catastrophic forgetting, we applied Parameter-Efficient Fine-Tuning (PEFT) using Low-Rank Adaptation (LoRA). The weight update matrix $\Delta W$ is decomposed into low-rank matrices $A$ and $B$:

$$W = W_0 + \Delta W = W_0 + \frac{\alpha}{r} (B \cdot A)$$

where:

- $W_0 \in \mathbb{R}^{d \times k}$ are the frozen weights of the attention query/key/value projection layers.
- $B \in \mathbb{R}^{d \times r}$ and $A \in \mathbb{R}^{r \times k}$ are the trainable low-rank adapters.
- $r \ll \min(d, k)$ is the low rank ($r = 16$), and $\alpha$ is a scaling hyperparameter.

This approach reduced trainable parameters by **$99.8\%$** while adapting the model to compile-safe SVRF syntax structures.

---

### Self-Reflection & Agentic Verification Loop

To overcome model hallucination, the Copilot runs in a closed self-reflection loop:

```
 Natural Language Specification ──────► [ LoRA-Fine-Tuned LLM ]
                                                │
                                                ▼
     [ Syntax Error Message ] ◄──── [ SVRF Linter / Compiler ]
               │                                │  (No errors)
               ▼                                ▼
  [ Iterative Prompt Refinement ]     Executable SVRF Rule Deck
```

1. **Generation**: The fine-tuned LLM generates a candidate SVRF rule block.
2. **Compilation**: The candidate block is piped into a local compiler linter.
3. **Self-Correction**: If the linter reports a syntax error, the compiler error logs (with line numbers and token mismatch descriptions) are extracted and appended to a system prompt. The model is prompted to rewrite the code to fix the specific error.

---

### Key Outcomes & Technical Impact

- **Developer Efficiency**: Reduced rule deck development cycles by **$40\%$** at Siemens EDA, translating complex physical specs to functional code blocks in seconds.
- **Syntactic Correctness**: Increased the compiler pass-rate of first-generation code from **$62\%$** to **$94\%$** using the agentic self-reflection compiler loop (typically converging within 3 iterations).
- **Tool Integration**: Designed a Model Context Protocol (MCP) server that links the linter engine to modern IDEs, providing developers with real-time, inline SVRF synthesis and verification feedback.
