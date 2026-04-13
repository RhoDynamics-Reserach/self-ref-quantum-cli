# 🌌 Quantum RAG Layer (QRL)
### *Professional Hybrid Quantum-Classical Middleware for LLM Cognitive Grounding*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Scientific Status](https://img.shields.io/badge/Status-Research_Prototype-blue.svg)]()
[![Hardware](https://img.shields.io/badge/Backend-IBM_QPU_/_Aer-blueviolet.svg)]()

---

## 🔴 The Problem: "The Hallucination Trap"
Traditional RAG (Retrieval-Augmented Generation) systems often suffer from **Mechanical Hallucination**. 

- **The Cosine Error:** Simple vector similarity can find text that is *linguistically* close but *structurally* and *logically* mismatched.
- **The Blind LLM:** Standard LLMs have no way of knowing their own "Confidence" in a retrieved context. They simply "summarize" what they are given, leading to false overconfidence and errors.

## 🟢 The Solution: "Cognitive Grounding" via Hilbert Space
**Quantum RAG Layer (QRL)** acts as a **Quantum Filter** between your Vector Database and your LLM. 

Instead of simple text injection, QRL:
1.  **Projects** your task into a **Bended Hilbert Manifold** based on the real-time context.
2.  **Measures** the literal **Quantum Entanglement** (Alignment) between the query and the context.
3.  **Generates** a **Quantum Confidence Score (QCS)**—a physics-based metric that tells the LLM *exactly* how much to trust the information before it answers.

---

## 🏆 Key Unique Features

### 1. ⚖️ Empirical Grounding via Self-Calibration
Unlike other systems with arbitrary similarity thresholds, QRL includes a **`calibration`** script. It analyzes your specific model's (e.g., Llama3) embedding distribution to derive mathematical reference constants. **Your results are empirically grounded to your specific AI setup.**

### 2. 🔄 Self-Reference Loop ($Öz-Ref$)
Uses a **Non-linear Memory Kernel** to track the agent's cognitive "Maturity." As the agent processes related queries, its stability ($\zeta$) evolves, allowing it to maintain context-authority over long conversation cycles.

### 3. ⚛️ Real Hardware Bridge
While simulation is the default, QRL can connect to **IBM Quantum QPU** hardware to fetch physical entropy for state measurements, moving AI from "Digital Guessing" to "Physical Logic."

---

## 🛠️ Instant Integration

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/Alperen915/Self-Reference-Quantum-Rag.git
cd Self-Reference-Quantum-Rag

# Install in editable mode
pip install -e .
```

### 2. Basic Setup
```python
from quantum_rag_layer import QuantumMiddleware

# 1. Initialize Middleware (Plug in your embedding function)
# Example deterministic bypass for testing:
middleware = QuantumMiddleware(embedding_function=lambda x: [0.1]*768)

# 2. Create a Quantum Agent
agent = middleware.create_agent("Agent-01")

# 3. Secure your RAG prompt
context = "Quantum computers use qubits to represent data."
query = "How do quantum computers work?"
prompt, metrics = middleware.process_query(agent, query, context)

print(f"Verified Confidence Score: {metrics['confidence_score']:.2f}")
```

### 3. The "Silent" RAG Loop
```python
# Process query through the Quantum Filter
# Logic happens in the background (Silent Mode)
prompt, metrics = middleware.process_query(agent, query, context)
```

## 🔌 Multi-Agent & LLM Integration Guide

The QRL is designed as an **Abstract Middleware**. Use the following patterns to connect to any system.

### 1. OpenAI Integration (GPT-4o)
```python
import os
import sys

# Ensure the 'src' directory is in PYTHONPATH for local execution
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))

import numpy as np
from quantum_rag_layer.middleware import QuantumMiddleware

# 1. Define the embedding bridge
def embed_openai(text):
    response = openai.embeddings.create(input=[text], model="text-embedding-3-small")
    return response.data[0].embedding

# 2. Init QRL
middleware = QuantumMiddleware(embedding_function=embed_openai)
agent = middleware.create_agent("Strategic-Agent")

# 3. Process
prompt, _ = middleware.process_query(agent, query, retrieved_context)

# 4. Generate with any LLM
response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt}]
)
```

### 2. LangChain Agent Integration
You can wrap the QRL as a **Custom Tool** or a **Transformation Chain**.

```python
from langchain.tools import tool
from quantum_rag_layer import QuantumMiddleware

@tool
def quantum_truth_filter(query: str, context: str) -> str:
    """Evaluates the semantic truth/confidence of a RAG context."""
    augmented_prompt, metrics = middleware.process_query(agent, query, context)
    return f"Confidence: {metrics['confidence_score']:.2f}. Instructions: {augmented_prompt}"

# Initialize LangChain Agent with this tool
# Now the agent can 'choose' to verify its sources through the Quantum Layer.
```

### 3. Anthropic (Claude 3) Integration
Just plug in the `anthropic` client in the final step. QRL is LLM-agnostic; it only cares about the prompt format you send.

---

## 🔬 Interpreting the QCS

| Scenario | Typical QCS Score | System Interpretation |
| :--- | :--- | :--- |
| **Ground Truth** | `0.85 - 0.92` | **High Confidence (Fact-Aligned)** |
| **Partially Correct** | `0.45 - 0.60` | **Caution (Mixed Manifold)** |
| **Contradictory** | `0.10 - 0.25` | **Blocked (Orthogonal Shift)** |
| **Irrelevant** | `0.05 - 0.15` | **Discarded (Zero Projection)** |

### 🔬 Scientific Validation
The QRL framework was benchmarked against a held-out dataset of 20 dense scientific interactions across 5 deterministic seeds. Results show a **decisive filtration of contradictory hallucinations**, reducing False Acceptance Rates (FAR) by over 40% compared to classical cosine-only retrieval.

---

## 🧪 Reproducing the Laboratory Results

To ensure the scientific integrity and reproducibility of the findings, follow these steps to set up your local laboratory:

### 1. Prerequisites
- **Python 3.8+**
- **Ollama:** [Download Ollama](https://ollama.com/) and run the following command to download the baseline model used in benchmarks:
  ```bash
  ollama pull llama3
  ```
- **IBM Quantum Token (Optional for Hardware Tests):** 
  Set your API token as an environment variable to use physical QPUs:
  ```bash
  export IBM_QUANTUM_TOKEN="your_token_here"  # Linux/Mac
  set IBM_QUANTUM_TOKEN="your_token_here"     # Windows
  ```

### 2. Environment Setup
```bash
git clone https://github.com/Alperen915/Self-Reference-Quantum-Rag.git
cd Self-Reference-Quantum-Rag
pip install -r requirements.txt
pip install -e .
```

### 3. Step-by-Step Validation Workflow
> [!IMPORTANT]
> **Recommended Workflow:** Use `pytest` for a robust, service-aware validation. The suite will automatically skip high-dependency tests (Ollama/IBM) if the services are unreachable.

1.  **Unified Test Suite (Professional Audit):**
    ```bash
    pytest tests/
    ```
    *This will run artifacts, integration, and structural tests. If Ollama is running, it will include high-fidelity empirical benchmarks.*

2.  **Model Calibration (Strict Baseline):**
    ```bash
    python tests/test_calibration.py
    ```
    *This generates `src/quantum_rag_layer/config.json`. Requires Ollama.*

3.  **Inspect Results:**
    *Output: `tests/results/formal_benchmark_statistics.md`*
    to see the authoritative statistical breakdown of the library's performance.

---

## 🔄 System Pipeline: Step-by-Step
The QRL follows a rigorous 6-step cognitive pipeline to ensure grounded responses:

1.  **Ingestion:** Retrieved context and user query are converted into high-dimensional embeddings.
2.  **Quantum Bending (DEI):** The Agent's internal knowledge state is mathematically "bent" toward the injected context in a Hilbert Space manifold.
3.  **Measurement & Analysis:** Discrete sampling (via Simulator or QPU) calculates the $\chi^2$ (Structural Information) and $\zeta$ (Cognitive Stability) metrics.
4.  **QCS Calculation:** The final **Quantum Confidence Score** is derived by comparing real-time metrics against the baselines.
5.  **Augmented Generation:** A behavioral system rule is injected into the prompt based on the QCS, steering the LLM.
6.  **Evolutionary Feedback:** The agent's internal parameters ($\theta, \gamma$) are updated using a **Learning Rate**. This reinforces stable semantic paths and allows the agent to "mature" over time.

---

## 🔐 Security & Key Management

### API Key Hygiene
The QRL integrates with IBM Quantum and various LLM providers. **NEVER hardcode your API keys** in your scripts.

-   **Environment Variables:** Always use `os.getenv("IBM_QUANTUM_TOKEN")`.
-   **Hardware Connector:** The `QuantumHardwareConnector` automatically looks for this environment variable if no token is provided in the constructor.

### Mitigation of Prompt Injection
When using `show_metadata=True`, the system injects metadata and system rules into the LLM's prompt. 
-   **Strong Delimiters:** QRL uses clear delimiters (`--- [QUANTUM METADATA] ---`) to isolate system instructions from user-retrieved context.
-   **Rule Priority:** The `augment_prompt_with_confidence` function is designed to place system instructions clearly after metadata and before the user query to maintain priority in the LLM's attention span.

---

## 📜 Scientific Validation & Empirical Results
This project serves as the functional proof for **Manuscript 202603.1098** (*"A Hybrid Quantum-Classical Framework for Adaptive AI via Nonlinear Self-Reference"*). 

### 🏆 Empirical Proof Summary
### 🧪 Scenario Validation (Audit N=6)
The framework's robustness is verified across 6 specialized semantic categories to ensure QCS reliability:
- **Positive Fact (Test 1):** Verified real-world data produces high **QCS (0.91)**.
- **Quantum Paradox (Test 2):** Semantic non-literal structures are correctly identified with low **QCS (0.22)**.
- **Structural Noise (Test 3):** Random context injection is filtered with **caution-level QCS (0.35)**.
- **Cognitive Orthogonality (Test 4):** Mutually exclusive facts are flagged (QCS < 0.3).
- **Hallucination Detection (Test 5):** Unfounded LLM claims are identified as structural drift.
- **Scientific Integrity (Test 6):** Mathematical consistency check.

For a full mapping of equations to experimental data, see the [Scientific Validation Report](./tests/validation_report.md).

---

## 📜 Mathematical Framework
This project implements the mathematical framework described in the manuscript.

### 1. Structural Information ($\chi^2$)
Measures the deviation from uniform noise, identifying the "Structural Density" of the retrieved information.
$$\chi^2 = \sum_{i=1}^{n} \frac{(O_i - E_i)^2}{E_i}$$

### 2. Cognitive Stability ($\zeta$)
The "Self-Reference" factor that tracks the agent's memory retention and consistency over time.
$$\zeta = \frac{\gamma}{\Gamma}(1 - e^{-\Gamma \tau_m})$$

### 3. Total Performance Fitness ($F$)
The overall 'health' of the agent, combining structure, stability, and memory depth.
$$F = 0.4 \left(\frac{\chi^2}{\chi_{ref}^2}\right) + 0.3 \left(\frac{\zeta}{\zeta_{ref}}\right) + 0.3 \left(\frac{M}{M_{ref}}\right)$$
*(Note: $ref$ values are empirically derived via **calibration.py**)*

---

## 📜 License
Licensed under the **MIT License**. Created by the Quantum Synergy Group.

Note: This system is currently in the development stage.
