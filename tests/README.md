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

## 🚀 The "Honesty" Workflow (V5.1 Optimized)

To ensure your RAG system is scientifically valid and not just "guessing":

#### Holistic Audit (Recommended)
```bash
pytest tests/
```
*This command uses the new robust infrastructure to discover all tests, handling service checks and skips automatically.*

#### Step-by-Step Methodology
If you prefer manual execution of individual components:

1.  **Calibrate your Model:**
    ```bash
    python tests/test_calibration.py
    ```
2.  **Sequential Drift Analysis:**
    ```bash
    python tests/test_drift.py
    ```
3.  **Formal Academic Benchmark:**
    ```bash
    python tests/run_academic_benchmark.py
    ```

---

## 🔬 Scientific Metrics Explained

*   **QCS (Quantum Confidence Score):** The probability that the task vector aligns with the blended knowledge manifold in Hilbert space. **High (>0.8)** = Strong structural alignment. **Low (<0.4)** = Potential Hallucination.
*   **Zeta ($\zeta$):** Cognitive stability. Tracks how well the agent maintains its persona/knowledge over sequential related queries.
*   **Chi-Square ($\chi^2$):** Measures the "Entropy" of the current state. Higher values indicate more structured information is being retrieved.
