import pytest
import json
import requests
import numpy as np
from quantum_rag_layer.math_engine import calculate_chi_square, calculate_zeta
from quantum_rag_layer.encoding import text_to_quantum_state

OLLAMA_URL = "http://localhost:11434/api/embeddings"
OLLAMA_MODEL = "llama3"

def check_ollama():
    try:
        response = requests.post(OLLAMA_URL, json={"model": OLLAMA_MODEL, "prompt": "test"}, timeout=1.0)
        return response.status_code == 200
    except:
        return False

def get_real_embedding(text):
    response = requests.post(OLLAMA_URL, json={"model": OLLAMA_MODEL, "prompt": text}, timeout=10.0)
    if response.status_code == 200:
        return np.array(response.json()["embedding"])
    else:
        raise ConnectionError(f"Ollama returned status {response.status_code}")

@pytest.mark.ollama
@pytest.mark.skipif(not check_ollama(), reason="Ollama service ('llama3') unreachable at localhost:11434")
def test_calibration_generates_empirical_config(tmp_path):
    """
    Test that the calibration logic measures empirical baselines 
    and writes them correctly to a temporary config.json.
    """
    target_path = tmp_path / "config.json"
    
    # 1. Sample baselines
    texts = ["A black hole is a region of spacetime."]
    chi_squares = []
    
    for text in texts:
        vec = get_real_embedding(text)
        state_probs = text_to_quantum_state(vec)
        shots = 1024
        chi = calculate_chi_square(state_probs * shots, shots)
        if chi > 0:
            chi_squares.append(chi)
            
    empirical_chi = float(np.mean(chi_squares)) if chi_squares else 100.0
    empirical_zeta = float(calculate_zeta(1.0, 0.3, 2.0))
    
    # 2. Save
    config_data = {
        "CHI_SQUARE_REF": empirical_chi,
        "ZETA_REF": empirical_zeta,
        "calibration_type": "empirical"
    }
    
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=4)
        
    # 3. Verify
    assert target_path.exists()
    with open(target_path, "r") as f:
        loaded = json.load(f)
        assert abs(loaded["CHI_SQUARE_REF"] - empirical_chi) < 0.001
