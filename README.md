# 🌌 Quantum RAG Layer (QRL)
### *Advanced Hybrid Quantum-Classical Middleware for LLM Cognitive Grounding*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)]()
[![Backend](https://img.shields.io/badge/Backend-Qiskit_/_Numpy-blueviolet.svg)]()

---

**Quantum RAG Layer (QRL)** is a specialized middleware designed to solve the "Mechanical Hallucination" problem in traditional RAG systems. Instead of simple vector-based text injection, QRL uses **Quantum Manifold Projection** to evaluate the semantic alignment between an Agent's core knowledge and retrieved context.

By mapping high-dimensional embeddings into a **Hilbert Space**, QRL generates a **Quantum Confidence Score (QCS)** that dynamically steers the LLM's response tone, authority, and skepticism.

---

## 🛠️ Instant Integration

QRL is designed to be "plug-and-play" with any LLM provider (OpenAI, Anthropic, Ollama, LangChain).

### 1. Installation
```bash
pip install ./quantum_rag_layer
```

### 2. Basic Setup
```python
from quantum_rag_layer.middleware import QuantumMiddleware

# Plug in any embedding function
middleware = QuantumMiddleware(embedding_function=lambda x: my_model.embed(x))

# Initialize a Quantum Agent with a base persona
agent = middleware.create_agent("Agent-01", "You are an expert in Physics.")
```

### 3. The RAG Loop (OpenAI Example)
```python
# Evaluate query and context through the Quantum Filter
prompt, metrics = middleware.process_query(agent, query, context)

# metrics['confidence_score'] is the derived authority (0.0 to 1.0)
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)
```

---

## 🧠 Core Engineering Concepts

### Dynamic Embedding Injection (DEI)
Traditional RAG blindly pastes context into a prompt. DEI "bends" the agent's internal state $|\psi_{agent}\rangle$ towards the context $|\psi_{context}\rangle$ before evaluating the task. This ensures the output is not just a summary, but a cognitively filtered synthesis.

### Quantum Confidence Score (QCS)
The QCS weighting system uses the **Synergy Integral ($S_{int}$)** logic based on:
1.  **Chi-Square ($\chi^2$):** Structural information density.
2.  **Zeta ($\zeta$):** Cognitive stability and historical consistency.
3.  **Projection:** Vector alignment in the reduced Hilbert manifold.

---

## 🔌 AI System Connectors

| System | Integration Method |
| :--- | :--- |
| **OpenAI / Anthropic** | Use `middleware.process_query` to wrap the user message before sending. |
| **LangChain** | Wrap your `RetrievalQA` chain result in a custom `TransformChain` that calls QRL. |
| **Ollama** | Directly use `requests` to call local API with the `augmented_prompt`. |

---

## ⚡ Hardware & Simulation
Choose your compute backend seamlessly:
*   **Simulator (Default):** Runs locally using `Qiskit Aer` and `Numpy` for low latency.
*   **Real Hardware:** Connect to **IBM Quantum QPU** by setting `IBM_QUANTUM_TOKEN` for absolute physical entropy in measurements.

---

## ⚠️ Limitations & Experimental Status
**QRL is currently in ALPHA stage.** Please be aware of the following:
*   **Information Bottleneck:** Downsampling embeddings (e.g. 4096 to 16/64 dims) involves intentional but lossy projection.
*   **Floating Point Drift:** Simulation metrics ($\chi^2$) may drift over extremely long conversation histories.
*   **Stability:** This library is a RESEARCH prototype. Complete operational stability and performance benchmarks against standard RAG on large-scale datasets are still in progress.
*   **Latency:** Running on real Quantum Hardware (IBM) will introduce significant network and queue latency.

---

## 📜 License
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.
