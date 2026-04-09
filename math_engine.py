import math
import numpy as np

# Core Constants from the Quantum Synergy Paper
C_0 = 1e6
CHI_SQUARE_REF = 310.0
ZETA_REF = 5.0
M_REF = 1000.0

def calculate_zeta(gamma: float, gamma_decoherence: float, tau_m: float) -> float:
    """
    Calculate the Zeta (\zeta) factor.
    Represents memory retention efficiency.
    \zeta = (\gamma / \Gamma) * (1 - e^{-\Gamma * \tau_m})
    """
    if gamma_decoherence <= 0:
        return 0.0 # Prevent division by zero
    
    return (gamma / gamma_decoherence) * (1 - math.exp(-gamma_decoherence * tau_m))

def calculate_chi_square(observed_counts: list, total_shots: int) -> float:
    """
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

def calculate_synergy_integral(chi_sq_a: float, chi_sq_b: float, zeta_a: float, zeta_b: float, theta_a: float, theta_b: float) -> float:
    """
    Calculate Synergy Integral (S_int) between Agent A and Agent B.
    S_int = (\chi^2_A * \chi^2_B * \zeta_A * \zeta_B * (1 - |\theta_A - \theta_B| / \pi)) / C_0
    """
    phase_diff = abs(theta_a - theta_b)
    alignment_factor = max(0.0, 1.0 - (phase_diff / math.pi))
    
    s_int = (chi_sq_a * chi_sq_b * zeta_a * zeta_b * alignment_factor) / C_0
    return s_int

def calculate_fitness(chi_square: float, zeta: float, memory_size: int) -> float:
    """
    Calculate Fitness (F).
    F = 0.4 * (\chi^2 / \chi_{ref}^2) + 0.3 * (\zeta / \zeta_{ref}) + 0.3 * (M / M_{ref})
    """
    f = 0.4 * (chi_square / CHI_SQUARE_REF) + \
        0.3 * (zeta / ZETA_REF) + \
        0.3 * (memory_size / M_REF)
    return f
