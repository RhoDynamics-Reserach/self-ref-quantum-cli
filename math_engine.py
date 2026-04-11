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
    return f
