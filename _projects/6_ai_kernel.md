---
layout: page
title: AI Kernel
description: "AI-First OS: Polyglot microkernel with Rust core and Python orchestration for AI workloads."
importance: 6
category: academic
github: https://github.com/AbanoubElkess/ai-kernel
img: /assets/img/ai_kernel_thumb.png
---

### Project Overview

Modern operating systems (such as Linux or Windows) are designed for general-purpose workloads, introducing considerable overhead when executing deep learning tasks. These overheads stem from frequent CPU-GPU context switches, heavy virtual file system layers, and CPU thread schedulers that do not account for tensor pipeline execution states. This leads to accelerator starvation and suboptimal hardware utilization.

To address these limitations, we designed and built **AI-Kernel**, a custom polyglot microkernel operating system. The system features a bare-metal kernel written in Rust for safety and raw speed, integrated with a high-level Python orchestration layer to manage tensor compute graph scheduling.

---

### Rust Microkernel & IPC Architecture

The core microkernel runs in supervisor mode, handling bare-metal hardware initialization, virtual memory paging, and low-latency task coordination.

#### 1. Hardware-Direct DMA Memory Mapping

To avoid virtual memory translation overhead and page-fault latency during massive tensor transfers, the kernel maps virtual pages directly to contiguous physical memory blocks using page-locked Direct Memory Access (DMA):

$$\mathcal{M}_{\text{DMA}}: \mathbf{V}_{\text{addr}} \to \mathbf{P}_{\text{addr}}$$

This mapping allows peripheral accelerators (like GPUs) to read and write system memory buffers directly without CPU intervention.

#### 2. Shared-Memory Lockless IPC

Microkernels rely heavily on Inter-Process Communication (IPC). To prevent locking bottlenecks, we implemented a lockless circular ring buffer in shared memory. It uses atomic compare-and-swap (CAS) operations to coordinate read/write pointers:

$$
\text{CAS}(P, V_{\text{expected}}, V_{\text{new}}) = \begin{cases}
\text{true} & \text{if } *P = V_{\text{expected}} \text{ (set } *P = V_{\text{new}}\text{)} \\
\text{false} & \text{otherwise}
\end{cases}
$$

This design achieves sub-microsecond IPC latency, preventing system message queues from stalling deep learning inference loops.

---

### Python Orchestration & PyO3 Bindings

Rather than implementing complex, evolving AI scheduling algorithms in compiled low-level code, we built a Python orchestration layer. This layer parses model execution graphs (e.g. ONNX, PyTorch) and manages execution pipelines.

```
  Python Orchestration (PyTorch / ONNX Graph Parser)
                        │
                        ▼ (PyO3 Direct Binding Calls)
  ┌────────────────────────────────────────────────────────┐
  │ Rust FFI Interface layer                                │
  │                                                        │
  │   #[pyfunction]                                        │
  │   fn schedule_tensor_op(op_id: u64) -> PyResult<u32>   │
  └────────────────────────────────────────────────────────┘
                        │
                        ▼ (Direct syscall / memory map)
         Rust Microkernel / Bare-Metal Driver
```

The connection between the Rust system calls and Python space is built using **PyO3** bindings, allowing zero-copy sharing of raw tensor arrays across the boundary.

---

### AI-Native Scheduling Formulation

Standard operating system schedulers (like Linux's Completely Fair Scheduler) optimize for interactive thread responsiveness. In contrast, the AI-Kernel scheduler optimizes for tensor pipeline throughput, maximizing the overlapping of memory transfers with compute executions:

$$\text{Throughput} = \max \sum_{i=1}^{M} \frac{\text{BatchSize}_i}{T_{\text{transfer}}(i) + T_{\text{compute}}(i) - T_{\text{overlap}}(i)}$$

where:

- $T_{\text{transfer}}(i)$ is the DMA transfer time of model weights and inputs.
- $T_{\text{compute}}(i)$ is the raw execution time on the accelerator.
- $T_{\text{overlap}}(i)$ is the time window where transfer and compute execute concurrently.

---

### Key Outcomes & Technical Impact

- **Accelerator Performance**: Improved GPU tensor pipeline utilization by **$22\%$** compared to standard Linux kernel baselines during heavy concurrent LLM and CNN inference runs.
- **IPC Efficiency**: Achieved message-passing latency of less than **$850\text{ ns}$**, removing microkernel communication overhead.
- **Proof-of-Concept**: Successfully compiled and booted on x86_64 hardware, implementing basic PCIe drivers to coordinate direct memory transfers between physical system RAM and external GPU buffers.
