import numpy as np
import math

class MemoryBuffer:
    """
    Self-Reference Memory Buffer. 
    Implements a non-linear memory kernel to allow past states 
    to influence current cognitive stability (Zeta).
    
    This is the core 'Öz-Referans' (Self-Reference) mechanism.
    """
    def __init__(self, tau_m: float = 2.0, max_history: int = 100):
        self.tau_m = tau_m
        self.max_history = max_history
        self.history = [] # Stores (timestamp, quantum_probability_distribution)
        self.current_t = 0
        
    def add_state(self, state_probabilities: np.ndarray):
        """Append the current quantum state to the self-reference memory."""
        self.history.append((self.current_t, state_probabilities))
        if len(self.history) > self.max_history:
            self.history.pop(0)
        self.current_t += 1
        
    def get_memory_effect(self, current_state: np.ndarray):
        """
        Calculates the memory kernel integral based on past states.
        Overlap with past successful states = higher cognitive stability.
        """
        if not self.history:
            return 0.0
            
        integral_sum = 0.0
        purity = np.sum(current_state ** 2)
        
        for tau, past_state in self.history[:-1]:
            # Kernel K(t - tau) = (1/tau_m) * e^-( (t - tau) / tau_m )
            dt = self.current_t - tau
            kernel = (1.0 / self.tau_m) * math.exp(-dt / self.tau_m)
            
            # Semantic overlap: Contrast between current state and memory path
            overlap = np.linalg.norm(current_state - past_state)
            
            integral_sum += kernel * overlap
            
        return purity * integral_sum

def update_stability_dynamically(zeta_base: float, memory_effect: float):
    """Adjust Zeta (cognitive stability) factor based on the actual memory kernel integral."""
    # Positive memory feedback loops stabilize the agent (boosts Zeta)
    return zeta_base * (1.0 + memory_effect)
