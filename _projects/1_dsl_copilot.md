---
layout: page
title: Domain Specific Language Copilot
description: Generative AI tool that automatically writes Standard Verification Rule Format (SVRF) language code from natural language prompts.
importance: 1
category: work
img: /assets/img/dsl_copilot_thumb.png
related_publications: true
toc:
  sidebar: left
---

### Project Overview

Physical verification rule decks for semiconductor layouts are traditionally written in proprietary Domain-Specific Languages (DSLs), most notably Siemens SVRF (Standard Verification Rule Format). These rule decks specify thousands of geometric, topological, and electrical constraints that a circuit design must satisfy to be manufacturable. Creating and maintaining these decks is a major bottleneck in semiconductor design-technology co-optimization (DTCO).

To address this challenge, we developed a specialized generative AI Copilot. The system translates natural language verification specifications directly into syntactically valid SVRF code blocks, utilizing a closed-loop validation engine to eliminate compiler and linter errors.

---

### Compiler Front-End & Grammar Parsing

Physical verification decks require absolute precision. Traditional LLMs fail because they lack an understanding of the strict formal grammar governing SVRF. We addressed this by integrating a formal compiler front-end.

#### 1. Context-Free Grammar Formulation

We constructed a formal Context-Free Grammar (CFG) for a subset of SVRF rules using ANTLR. The grammar is defined as a 4-tuple:

$$G = (V, \Sigma, R, S)$$

where:

- $V$ is the set of non-terminal SVRF structures (such as rule blocks, check environments, or layer operations).
- $\Sigma$ is the set of terminal layout operation tokens (such as `EXT`, `INT`, `ENC`, `CONNECT`, `NOT`, `AND`).
- $R$ represents the production rules mapping statements to structural layout constraints.
- $S$ is the start symbol.

#### 2. Abstract Syntax Tree (AST) Generation

The parser processes natural-language-generated SVRF candidates into an AST. This AST representation is passed through a compiler visitor pattern that checks:

- **Layer References**: Ensures all input layers are declared and connected.
- **Dimensional Correctness**: Validates that distance parameters use correct units (e.g., microns) and obey physical limits.
- **Topological Integrity**: Confirms that Boolean layer operations do not yield empty sets.

---

### Tokenizer Alignment & Vocabulary Extension

A major challenge in using pre-trained code models (such as StarCoder) for proprietary DSLs is the vocabulary mismatch. Standard tokenizers split specialized SVRF keywords into meaningless sub-tokens (e.g., `SVRF_RULE` becomes `SV`, `RF`, `_`, `RU`, `LE`).

#### 1. Special Token Injection

We extended the model's tokenizer vocabulary by adding 150+ custom keywords (e.g., `EXT[DEPORT]`, `CONNECT`, `BIAS`, `SRAF`). This prevented fragmentation and allowed the model to represent complex operations as single embedding vectors, increasing context window efficiency.

#### 2. Positional and Attention Mask Alignment

To handle the highly nested structure of SVRF decks (where checks are nested inside outer cells), we adjusted the self-attention mask to restrict attention flow, forcing the model to resolve local geometric rules before looking at global cell boundary definitions.

---

### Low-Rank Adaptation (LoRA) Fine-Tuning

To specialize the base code model (e.g., StarCoder-15B) on proprietary, sparse SVRF data without catastrophic forgetting, we applied Parameter-Efficient Fine-Tuning (PEFT) using Low-Rank Adaptation (LoRA).

#### 1. Low-Rank Matrix Decomposition

The weight update matrix $\Delta W$ in the self-attention projection layers is factored into two low-rank matrices $A$ and $B$:

$$W = W_0 + \Delta W = W_0 + \frac{\alpha}{r} (B \cdot A)$$

where:

- $W_0 \in \mathbb{R}^{d \times k}$ are the frozen weights of the attention query/key/value projection layers.
- $B \in \mathbb{R}^{d \times r}$ and $A \in \mathbb{R}^{r \times k}$ are the trainable low-rank adapters.
- $r \ll \min(d, k)$ is the low rank ($r = 16$).
- $\alpha$ is a scaling hyperparameter ($\alpha = 32$).

#### 2. Training Hyperparameters

- **Base Model**: StarCoder-15B (optimized for code synthesis).
- **Learning Rate**: $2 \times 10^{-4}$ with a cosine learning rate scheduler.
- **Batch Size**: 64 sequences (sequence length of 2048 tokens).
- **Optimizer**: AdamW with weight decay of 0.01.
- **Compute**: Trained on 8x NVIDIA H100 GPUs using DeepSpeed ZeRO-Stage 3 for model partitioning.

---

### Closed-Loop Self-Reflection Architecture

To overcome model hallucination and guarantee compilation, the Copilot executes a multi-step agentic cycle:

```
 Natural Language Specification ──────► [ LoRA-Fine-Tuned LLM ]
                                                │
                                                ▼
     [ Syntax Error Message ] ◄──── [ SVRF Linter / Compiler ]
               │                                │  (No errors)
               ▼                                ▼
  [ Iterative Prompt Refinement ]     Executable SVRF Rule Deck
```

1. **Candidate Generation**: The fine-tuned LLM synthesizes a candidate SVRF rule block.
2. **Dynamic Compilation**: The block is piped into a local headless verification compiler.
3. **Error Ingestion**: If the compiler fails, the raw compiler log is parsed. The system extracts the line number, the violating token, and the expected syntax.
4. **Self-Correction**: A prompt is built enclosing the original spec, the failed code, and the compiler errors. The model generates a corrected draft. This loop continues until compilation succeeds (capped at 5 attempts).

---

### Key Outcomes & Technical Impact

- **Developer Efficiency**: Reduced physical verification rule deck writing cycles by **$40\%$** at Siemens EDA, translating complex physical specs to functional code blocks in seconds.
- **Syntactic Correctness**: Increased the compiler pass-rate of first-generation code from **$62\%$** to **$94\%$** using the agentic self-reflection compiler loop (typically converging within 3 iterations).
- **Tool Integration**: Designed a Model Context Protocol (MCP) server that links the linter engine to modern IDEs, providing developers with real-time, inline SVRF synthesis and verification feedback.
