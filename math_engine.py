import math
import numpy as np

import os
import json

# --- CORE SCIENTIFIC REFERENCE CONSTANTS ---
# Defaults are based on the initial 202603.1098 research data.
# BUT: These will be overwritten by 'calibration.py' for model-specific accuracy.

CHI_SQUARE_REF = 310.0
ZETA_REF = 5.0
M_REF = 1000.0

# Dynamic Calibration Loader
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")
if os.path.exists(CONFIG_FILE):
    try:
        with open(CONFIG_FILE, "r") as f:
            _cfg = json.load(f)
            CHI_SQUARE_REF = _cfg.get("CHI_SQUARE_REF", CHI_SQUARE_REF)
            ZETA_REF = _cfg.get("ZETA_REF", ZETA_REF)
            M_REF = _cfg.get("M_REF", M_REF)
    except:
        pass # Fallback to theoretical paper defaults

def calculate_zeta(gamma: float, gamma_decoherence: float, tau_m: float) -> float:
    r"""
    Calculate the Zeta (\zeta) factor.
    Represents memory retention efficiency.
    \zeta = (\gamma / \Gamma) * (1 - e^{-\Gamma * \tau_m})
    """
    if gamma_decoherence <= 0:
        return 0.0 # Prevent division by zero
    
    return (gamma / gamma_decoherence) * (1 - math.exp(-gamma_decoherence * tau_m))

def calculate_chi_square(observed_counts: list, total_shots: int) -> float:
    r"""
    Calculate the \chi^2 metric.
    Measures deviation from uniform distribution (structural information).
    """
    n_states = len(observed_counts)
    if n_states == 0: return 0.0
    expected = total_shots / n_states
    
    chi_square = 0.0
    for obs in observed_counts:
        chi_square += ((obs - expected) ** 2) / expected
        
    return chi_square

def calculate_fitness(chi_square: float, zeta: float, memory_size: int) -> float:
    r"""
    Calculate Fitness (F).
    F = 0.4 * (\chi^2 / \chi_{ref}^2) + 0.3 * (\zeta / \zeta_{ref}) + 0.3 * (M / M_{ref})
    """
    f = 0.4 * (chi_square / CHI_SQUARE_REF) + \
        0.3 * (zeta / ZETA_REF) + \
        0.3 * (memory_size / M_REF)
    return min(f, 1.0) # Cap at 1.0 for normalized scaling

def calculate_self_ref_signal(state_vector: np.ndarray) -> float:
    """
    Measures the Self-Reference signal (Phi).
    Determined by the coherence of the state relative to the pointer basis.
    """
    if state_vector is None or len(state_vector) == 0:
        return 0.0
    # Signal is the ratio of L2 norm of off-diagonal elements (approx)
    # Simply using the standard deviation of expectations for PoC
    return float(np.std(np.abs(state_vector)))

def evolve_parameters(current_theta: float, current_gamma: float, fitness: float, learning_rate: float):
    """
    Calculates the evolutionary shift for agent parameters.
    Simulates the 'Offline Evolution' described in the paper.
    """
    # Fitness > 0.7 triggers positive reinforcement
    # Fitness < 0.3 triggers negative mutation
    
    delta_theta = (fitness - 0.5) * learning_rate * 2.0
    delta_gamma = (fitness - 0.5) * learning_rate * 0.5
    
    new_theta = current_theta + delta_theta
    new_gamma = current_gamma + delta_gamma
    
    # Bound-check to keep parameters within physical/stable ranges
    new_theta = max(-math.pi, min(math.pi, new_theta))
    new_gamma = max(0.1, min(10.0, new_gamma))
    
    return new_theta, new_gamma
