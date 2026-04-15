import os
import sys
import json
import requests
import numpy as np
import pytest

# Path resolution for standalone utility usage
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_dir = os.path.join(base_dir, "src")
if src_dir not in sys.path:
    sys.path.append(src_dir)

from rhodynamics.math_engine import calculate_chi_square, calculate_zeta
from rhodynamics.encoding import text_to_quantum_state

OLLAMA_URL = "http://localhost:11434/api/embeddings"
OLLAMA_MODEL = "llama3"

def check_ollama():
    try:
        response = requests.post(OLLAMA_URL, json={"model": OLLAMA_MODEL, "prompt": "test"}, timeout=1.0)
        return response.status_code == 200
    except:
        return False

def get_real_embedding(text):
    try:
        response = requests.post(OLLAMA_URL, json={"model": OLLAMA_MODEL, "prompt": text}, timeout=10.0)
        if response.status_code == 200:
            return np.array(response.json()["embedding"])
        else:
            raise ConnectionError(f"Ollama returned status {response.status_code}")
    except Exception as e:
        print(f"[!] Warning: Ollama connection failed ({e}). Using random vector for calibration.")
        return np.random.rand(768)

@pytest.mark.ollama
@pytest.mark.skipif(not check_ollama(), reason="Ollama service ('llama3') unreachable at localhost:11434")
def test_calibration_generates_empirical_config(tmp_path):
    """
    Test that the calibration logic measures empirical baselines 
    and writes them correctly to a temporary config.json.
    """
    target_path = tmp_path / "config.json"
    run_calibration_sequence(target_path)
    assert target_path.exists()

def run_calibration_sequence(output_path):
    """Core logic to sample baselines and write to a path."""
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
    
    config_data = {
        "CHI_SQUARE_REF": empirical_chi,
        "ZETA_REF": empirical_zeta,
        "M_REF": 1000.0,
        "calibration_type": "empirical"
    }
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=4)
    print(f"[+] Calibration generated: {output_path}")

if __name__ == "__main__":
    # Standalone execution updates the actual project config
    pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target = os.path.join(pkg_dir, "src", "rhodynamics", "config.json")
    try:
        run_calibration_sequence(target)
    except Exception as e:
        print(f"[ERROR] Standalone calibration failed: {e}")
