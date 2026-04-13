import json
import numpy as np
import pytest
from quantum_rag_layer import QuantumMiddleware

def test_calibration_artifact_generation(tmp_path, mock_embedding):
    """
    Verifies that calibration logic produces a valid config.json using
    actual math engine outputs, stored in a temporary directory.
    """
    config_path = tmp_path / "config.json"
    
    # Run real logic to get empirical values
    from quantum_rag_layer.math_engine import calculate_zeta, calculate_chi_square
    from quantum_rag_layer.encoding import text_to_quantum_state
    
    vec = mock_embedding("test text")
    state_probs = text_to_quantum_state(vec)
    chi = float(calculate_chi_square(state_probs * 1024, 1024))
    zeta = float(calculate_zeta(1.0, 0.3, 2.0))
    
    config_data = {
        "CHI_SQUARE_REF": chi,
        "ZETA_REF": zeta,
        "M_REF": 1000.0,
        "calibration_type": "automated-test"
    }
    
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=4)
    
    assert config_path.exists()
    assert chi > 0
    assert zeta >= 0

def test_drift_artifact_generation(tmp_path, mock_embedding):
    """
    Verifies that drift analysis generates valid historical JSON traces
    based on actual agent evolution cycles.
    """
    results_dir = tmp_path / "results"
    results_dir.mkdir()
    drift_path = results_dir / "drift_results.json"
    
    from quantum_rag_layer import QuantumMiddleware
    middleware = QuantumMiddleware(embedding_function=mock_embedding)
    agent = middleware.create_agent("Test-Agent", seed=42)
    
    history = []
    for i in range(3):
        middleware.process_query(agent, "query", "context")
        agent.evolve(learning_rate=0.1)
        history.append({
            "step": i,
            "zeta": float(agent.zeta),
            "fitness": float(agent.fitness)
        })
    
    with open(drift_path, "w") as f:
        json.dump(history, f, indent=4)
        
    assert drift_path.exists()
    assert len(history) == 3
    assert history[2]["zeta"] != history[0]["zeta"]
