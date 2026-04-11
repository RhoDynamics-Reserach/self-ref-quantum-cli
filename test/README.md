# 🧪 Quantum RAG Layer: Scientific Validation & Audit Suite

This directory contains the tools required to objectively validate the **Quantum RAG Layer (QRL)** against your specific LLM environment.

## 📂 Laboratory Structure

### Core Tools
*   **`calibration.py`**: ❗ **RUN THIS FIRST.** It analyzes your model's embedding distribution (e.g., Llama3) and generates a `config.json` with objective reference constants. This prevents "Data Shifting" bias.
*   **`scientific_benchmark.py`**: The primary "Honesty Test". Compares Classic RAG vs. Quantum RAG across 6 diverse scenarios, including hallucination traps and semantic collisions.
*   **`qpu_experiment_runner.py`**: Connects to **IBM Quantum** for real-world QPU execution.

### Results & Proofs (`results/`)
*   `objective_results.json`: Raw telemetry data from the latest audit.
*   `objective_validation.png`: Visual proof of how QCS distinguishes between semantic entanglement and random noise.

---

## 🚀 The "Honesty" Workflow

To ensure your RAG system is scientifically valid and not just "guessing":

1.  **Calibrate your Model:**
    ```bash
    python test/calibration.py
    ```
2.  **Run the Objective Audit:**
    ```bash
    python test/scientific_benchmark.py
    ```
3.  **Inspect the Manifold:**
    Check `results/objective_validation.png`. Look for high QCS in "Positive" cases and attenuated QCS in "Out of Context" cases.

---

## 🔬 Scientific Metrics Explained

*   **QCS (Quantum Confidence Score):** The probability that the task vector aligns with the blended knowledge manifold in Hilbert space. **High (>0.8)** = Strong structural alignment. **Low (<0.4)** = Potential Hallucination.
*   **Zeta ($\zeta$):** Cognitive stability. Tracks how well the agent maintains its persona/knowledge over sequential related queries.
*   **Chi-Square ($\chi^2$):** Measures the "Entropy" of the current state. Higher values indicate more structured information is being retrieved.
