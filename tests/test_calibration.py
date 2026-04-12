import pytest
import numpy as np

from quantum_rag_layer.math_engine import calculate_chi_square, calculate_zeta
from quantum_rag_layer.encoding import text_to_quantum_state

# Deterministic Embedding to prevent Random Fallbacks
def get_deterministic_embed(text_length):
    """
    Replaces Ollama HTTP calls and np.random.rand() fallbacks.
    Ensures 100% reproducible test conditions for peer reviewers.
    """
    np.random.seed(text_length)
    return np.random.uniform(0.1, 1.0, 768)

def test_calibration_baseline_generation():
    """
    Validates that the initialization math produces physically valid
    baselines for Chi-Square and Zeta self-reference without network noise.
    """
    sample_lengths = [32, 64, 128]
    chi_squares = []
    
    for length in sample_lengths:
        vec = get_deterministic_embed(length)
        state_probs = text_to_quantum_state(vec)
        
        shots = 1024
        # Deterministic extraction
        chi = calculate_chi_square(state_probs * shots, shots)
        assert chi > 0.0, f"Chi square must be strictly positive, got {chi}"
        chi_squares.append(chi)
        
    chi_ref = np.mean(chi_squares)
    zeta_ref = calculate_zeta(1.0, 0.3, 2.0)
    
    assert chi_ref > 0.0
    # Actual calculation: (1.0 / 0.3) * (1 - exp(-0.6)) approx 1.5039
    assert abs(zeta_ref - 1.5039) < 0.001
