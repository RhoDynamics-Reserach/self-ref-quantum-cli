# 🌌 Quantum RAG Layer (QRL)
### *Professional Hybrid Quantum-Classical Middleware for LLM Cognitive Grounding*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Scientific Status](https://img.shields.io/badge/Status-Validated_PoC-green.svg)]()
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

### 1. ⚖️ Objectivity via Self-Calibration
Unlike other systems with arbitrary similarity thresholds, QRL includes a **`calibration.py`** module. It analyzes your specific model's (e.g., Llama3) embedding distribution to derive objective reference constants. **Your results are 100% objective to your specific AI setup.**

### 2. 🔄 Self-Reference Loop ($Öz-Ref$)
Uses a **Non-linear Memory Kernel** to track the agent's cognitive "Maturity." As the agent processes related queries, its stability ($\zeta$) evolves, allowing it to maintain context-authority over long conversation cycles.

### 3. ⚛️ Real Hardware Bridge
While simulation is the default, QRL can connect to **IBM Quantum QPU** hardware to fetch physical entropy for state measurements, moving AI from "Digital Guessing" to "Physical Logic."

---

## 🛠️ Instant Integration

### 1. Installation
```bash
pip install ./quantum_rag_layer
```

### 2. Basic Setup
```python
from quantum_rag_layer import QuantumMiddleware, QuantumHardwareConnector

# 1. Initialize Middleware (Plug in any embedding function)
middleware = QuantumMiddleware(embedding_function=my_model.embed)

# 2. OPTIONAL: Calibrate first (See 'test/calibration.py')
# 3. Create a Quantum Agent
agent = middleware.create_agent("Agent-01", "You are an expert in Physics.")
```

### 3. The "Silent" RAG Loop
```python
# Process query through the Quantum Filter
# Logic happens in the background (Silent Mode)
prompt, metrics = middleware.process_query(agent, query, context)

## 🔌 Multi-Agent & LLM Integration Guide

The QRL is designed as an **Abstract Middleware**. Use the following patterns to connect to any system.

### 1. OpenAI Integration (GPT-4o)
```python
import openai
from quantum_rag_layer import QuantumMiddleware

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

## 🔬 Interpreting the QCS (Quality Gate)

| QCS Score | Interpretation | Action Taken |
| :--- | :--- | :--- |
| **0.80 - 1.00** | **Total Alignment.** Question and Context are "Entangled." | LLM speaks with absolute authority. |
| **0.40 - 0.79** | **Stable Alignment.** Context is relevant but has nuances. | LLM answers clearly but follows standard procedures. |
| **0.00 - 0.39** | **Structural Mismatch.** High Hallucination Risk! | LLM expresses hesitation, doubt, and extreme caution. |

---

## 📂 Laboratory & Validation
Run the objective audit to prove the system's performance:
1.  **Calibrate:** `python test/calibration.py`
2.  **Benchmark:** `python test/scientific_benchmark.py`
3.  **View Proof:** Check `test/results/objective_validation.png`

## 🔄 System Pipeline: Step-by-Step
The QRL follows a rigorous 5-step cognitive pipeline to ensure grounded responses:

1.  **Ingestion:** Retrieved context and user query are converted into high-dimensional embeddings.
2.  **Quantum Bending (DEI):** The Agent's internal knowledge state is mathematically "bent" toward the injected context in a Hilbert Space manifold.
3.  **Measurement & Analysis:** Discrete sampling (via Simulator or QPU) calculates the $\chi^2$ (Structural Information) and $\zeta$ (Cognitive Stability) metrics.
4.  **QCS Calculation:** The final **Quantum Confidence Score** is derived by comparing real-time metrics against the objectively calibrated reference baseline.
5.  **Augmented Generation:** A behavioral system rule is injected into the prompt based on the QCS, steering the LLM's level of authority and skepticism.

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

## 📜 Scientific Basis & Mathematical Framework
This project implements the mathematical framework described in **Manuscript 202603.1098** (*"A Hybrid Quantum-Classical Framework for Adaptive AI"*).

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
