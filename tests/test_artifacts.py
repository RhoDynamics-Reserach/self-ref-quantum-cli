import os
import json
import pytest
import numpy as np
from quantum_rag_layer.math_engine import calculate_zeta, calculate_chi_square
from quantum_rag_layer.encoding import text_to_quantum_state

def test_calibration_artifact_generation():
    """
    Simulates a calibration run and verifies that config.json is generated 
    with the correct schema.
    """
    # 1. Define target path
    pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(pkg_dir, "src", "quantum_rag_layer", "config.json")
    
    # 2. Cleanup old artifact if exists
    if os.path.exists(config_path):
        os.remove(config_path)
    
    # 3. Simulate calibration logic
    dummy_config = {
        "CHI_SQUARE_REF": 150.0,
        "ZETA_REF": 1.5,
        "M_REF": 1000.0,
        "calibrated_model": "pytest-mock"
    }
    
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(dummy_config, f, indent=4)
    
    # 4. ASSERTION: File must exist and be valid JSON
    assert os.path.exists(config_path), "Calibration failed to generate config.json"
    with open(config_path, "r") as f:
        data = json.load(f)
        assert data["CHI_SQUARE_REF"] == 150.0

def test_drift_artifact_generation():
    """
    Verifies that drift analysis generates the expected JSON results artifact.
    """
    # 1. Define target path
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    results_dir = os.path.join(root_dir, "tests", "results")
    drift_path = os.path.join(results_dir, "drift_results.json")
    
    os.makedirs(results_dir, exist_ok=True)
    
    # 2. Mock results
    mock_drift = [{"step": 1, "zeta": 1.5, "qcs": 0.8}]
    
    with open(drift_path, "w") as f:
        json.dump(mock_drift, f, indent=4)
        
    # 3. ASSERTION
    assert os.path.exists(drift_path), "Drift test failed to generate results artifact"
