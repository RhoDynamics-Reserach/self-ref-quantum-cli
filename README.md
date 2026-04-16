# 🌌 rhodynamics-lab-cli
### *Quantum Cognitive Grounding & Epistemic Filtration for Large Language Models*

[![Paper: Preprint](https://img.shields.io/badge/Paper-Preprint_202603.1098-red.svg)](https://www.preprints.org/manuscript/202603.1098)
[![Status: Advanced Prototype](https://img.shields.io/badge/Status-Advanced_Research_Prototype-orange.svg)]()
[![Hardware](https://img.shields.io/badge/Backend-IBM_QPU-blueviolet.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📜 Scientific Core (Manuscript 202603.1098)
This terminal serves as the functional proof of concept for the paper:
**"A Hybrid Quantum-Classical Framework for Adaptive AI via Nonlinear Self-Reference"**
[Access Full Manuscript](https://www.preprints.org/manuscript/202603.1098)

---

## 🏛️ Project Archetype: Beyond Vector Search
Standard RAG systems rely on **Geometric Similarity (Cosine)**, which is fundamentally flawed for logical validation. A text can be linguistically similar to a query but logically contradictory.

**RhoDynamics** introduces the **Quantum Hilbert Filter**. It projects information into a bended Hilbert manifold to measure the **Quantum Confidence Score (QCS)**. This physics-based metric detects semantic drift and "Epistemic Hallucinations" that classical similarity thresholds simply cannot see.

---

## 🛡️ The 'Silent Guardian' Protocol
The system operates in a **Non-Invasive Observation** mode.
1.  **Continuous Analysis**: QCS is calculated for every response in the background.
2.  **Adaptive Intervention**: 
    - **Confident State (QCS >= 0.5)**: Silent execution. The LLM produces high-fidelity responses.
    - **Risk State (QCS < 0.5)**: The **Silent Guardian** triggers. It reveals the agent's **Internal Monologue** and forces the LLM to adopt a skeptical persepctive on the input.

---

## ⚙️ System Workflow: The Quantum Filtration Loop

The RhoDynamics architecture follows a 5-stage sequential loop to ensure absolute cognitive grounding.

```mermaid
graph TD
    A[User Query & Context] --> B[Quantum State Encoding]
    B --> C{Hilbert Manifold Bending}
    C --> D[QCS Calculation]
    D --> E{Silent Guardian Trigger}
    E -- QCS < 0.5 --> F[Red Alert & Monologue Disclosure]
    E -- QCS >= 0.5 --> G[Authoritative LLM Output]
    F --> H[Adaptive Self-Reference Evolution]
    G --> H
    H --> I[Vault Persistence]
```

### 1. Ingestion & Encoding
The query and retrieved context are converted into high-dimensional embedding vectors, which are then mapped to quantum state amplitudes/phases.

### 2. Hilbert Manifold Bending
The agent's internal knowledge base acts as a "Base Manifold." The injected context is applied as a non-linear operator, "bending" the manifold. Any logical inconsistency creates measurable **Quantum Stress**.

### 3. Metric Extraction (QCS)
Numerical scores ($\zeta, \chi^2$) are extracted from the bended state. The **Quantum Confidence Score (QCS)** determines the truth-value probability.

### 4. Silent Guardian Intervention
If QCS is below the **0.40 - 0.50 risk threshold**, the system interrupts the LLM's default behavior, injecting skepticism and revealing the agent's internal reasoning (Monologue).

### 5. Adaptive Evolution
Regardless of the outcome, the interaction data is used to update the agent's **Zeta ($\zeta$)** and **Fitness** parameters, hardening the manifold against future drift.

---

## ⌨️ Research Terminal Mastery (CLI)

The `rhodynamics-lab-cli` is a professional-grade research station.

### 🏁 Quick Start: Entering the Lab
```bash
rhodynamics-cli
```

### 🛠️ Step-by-Step Research Cycle

| Phase | Command Syntax | Description |
| :--- | :--- | :--- |
| **1. Grounding** | `config hardware ibm_token <key>` | Link the physical **IBM QPU** bridge. |
| **2. Provider** | `config <engine> <model> [key]` | Set LLM (Ollama, Anthropic, GPT-4, Gemini). |
| **3. Synthesis** | `create <Name> \| <Objective>` | Synthesize a new persistent specialist agent. |
| **4. Synergy** | `fuse <A> <B> \| <NewName>` | **Entangle** two knowledge bases into a Synergy Master. |
| **5. Inference** | `query <Agent> \| <Task> \| [Context]`| Execute a quantum-grounded research cycle. |
| **6. Evolution** | `status` | Audit Zeta ($\zeta$) and Fitness of the vault nodes. |
| **7. Analytics** | `research <AgentName>` | Generate academic evolution plots (PNG). |
| **8. Export** | `export <AgentName>` | Dump the matured **Gold Asset** (.json). |

---

## 🌀 Synergy & Agent Entanglement

The `fuse` command is not a simple text concatenation; it is an **Entanglement Operation** performed on the agent's Hilbert Manifolds.

### The Mechanism
When two specialists (e.g., a Physicist and a Coder) are fused, RhoDynamics calculates the **Synergy Integral ($S_{int}$)**. This metric measures the **Constructive Interference** between their semantic states.
- **Entangled State**: The resulting agent shares a single co-dependent probability distribution, allowing for multi-disciplinary reasoning without context switching.
- **S_int > 0.5**: High Synergy. The agents' perspectives are mutually reinforcing.
- **S_int < 0.3**: Destructive Interference. The system has detected a fundamental epistemic conflict between the agents' base rules.

---

## 🔬 Empirical Audit: 20-Scenario Integrity Test
Our final scientific audit (N=20) demonstrates the system's ability to discriminate between facts and hallucinations with high statistical confidence.

### 📈 Statistical Performance Table
| Archetype | Standard Cosine | **RhoDynamics QCS** | Result |
| :--- | :--- | :--- | :--- |
| **Ground Truth** | 0.656 | **0.829 (Avg)** | [bold green]VERIFIED[/bold green] |
| **Hallucination** | 0.633 | **0.261 (Avg)** | [bold red]BLOCKED[/bold red] |
| **Near-Miss** | 0.504 | **0.221 (Avg)** | [bold red]BLOCKED[/bold red] |
| **Irrelevant** | 0.423 | **0.187 (Avg)** | [bold red]BLOCKED[/bold red] |

### 📊 Visual Evidence: Cognitive Hardening
![Stability Evolution](docs/gold_stability_evolution.png)

*Figure 1: Autonomous Cognitive Stability ($\zeta$) growth. The agent demonstrates "Knowledge Hardening" over 20+ dense semantic steps, consistently evolving toward higher logical resilience.*

![QCS Discrimination](docs/hardware_honesty_test.png)

*Figure 2: QCS vs. Similarity. Notice the sharp gap between verified ground truth and contradictory hallucinations, providing a clear "Epistemic Guardrail" for the LLM.*

---

## 🏛️ Open Source Research Community

RhoDynamics is a collaborative laboratory. We invite researchers and engineers to help us redefine AI grounding.

*   **[Researcher Contribution Guide](./CONTRIBUTING.md)**: How to add new metrics and adapters.
*   **[Community Agent Showcase](./showcase/README.md)**: Explore and share matured "Gold Assets" from other researchers.
*   **[Scientific Roadmap](./ROADMAP.md)**: Our vision for the future of epistemic AI.

---

## 💎 The 'Gold Asset' Protocol
The library includes pre-matured **"Gold Assets"** (Serialized Cognitive States) that have been evolved on physical IBM hardware.
- **`Synergy_Master_Gold.rho.json`**: Optimized stability ($\zeta=3.36$) for multidisciplinary research.

---

## 🧪 Installation
```bash
pip install rhodynamics-lab-cli
# Or from source
pip install -e .
```

---

## 📜 Stage and License
Licensed under **MIT**. This project is currently an **Advanced Research Prototype (v2.6.0)**. Use for academic and high-integrity AI research.
