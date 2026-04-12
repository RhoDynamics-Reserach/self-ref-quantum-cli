# 🧪 Quantum RAG Layer: Scientific Validation & Audit Suite

This directory contains the tools required to objectively validate the **Quantum RAG Layer (QRL)** against your specific LLM environment.

## 📂 Laboratory Structure

### Core Tools
*   **`tests/test_calibration.py`**: ❗ **RUN THIS FIRST.** It analyzes your model's embedding distribution (e.g., Llama3) and generates a `config.json` with objective reference constants. 
*   **`tests/test_scientific_benchmark.py`**: The primary "Honesty Test". Compares Classic RAG vs. Quantum RAG across 6 diverse scenarios.
*   **`tests/test_drift.py`**: Validates evolutionary stability over sequential interactions.
*   **`tests/test_integration.py`**: Full end-to-end chatbot simulation and smoke test.

### Results & Proofs (`tests/results/`)
*   `qpu_final_benchmark.json`: Raw telemetry data from the latest audit.
*   `final_evolution_plot.png`: Visual proof of how stability ($\zeta$) adapts to context.
*   `qcs_graph.png`: Differentiates between validity and paradox noise.

---

## 🚀 The "Honesty" Workflow

To ensure your RAG system is scientifically valid and not just "guessing":

1.  **Calibrate your Model:**
    ```bash
    python tests/test_calibration.py
    ```
2.  **Run the Objective Audit:**
    ```bash
    python tests/test_scientific_benchmark.py
    ```
3.  **Inspect the Manifold:**
    Check `tests/results/qcs_graph.png`. Look for high QCS in "Positive" cases and attenuated QCS in "Out of Context" cases.

---

## 🔬 Scientific Metrics Explained

*   **QCS (Quantum Confidence Score):** The probability that the task vector aligns with the blended knowledge manifold in Hilbert space. **High (>0.8)** = Strong structural alignment. **Low (<0.4)** = Potential Hallucination.
*   **Zeta ($\zeta$):** Cognitive stability. Tracks how well the agent maintains its persona/knowledge over sequential related queries.
*   **Chi-Square ($\chi^2$):** Measures the "Entropy" of the current state. Higher values indicate more structured information is being retrieved.
