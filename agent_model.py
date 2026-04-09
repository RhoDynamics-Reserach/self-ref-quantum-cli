import random
import numpy as np
from .math_engine import calculate_zeta, calculate_fitness, calculate_chi_square
from .memory import MemoryBuffer, update_stability_dynamically

class BaseQuantumAgent:
    """
    Lightweight, standalone Agent Model.
    Designed for easy injection into existing chatbot frameworks.
    
    Contains both the semantic state (knowledge_vector) 
    and the cognitive stability metrics (Zeta, Chi^2).
    """
    def __init__(self, name: str, knowledge_vector: np.ndarray = None):
        self.name = name
        
        # 1. Cognitive Parameters
        self.gamma = random.uniform(0.5, 1.5) # Coupling factor
        self.gamma_decoherence = random.uniform(0.1, 0.5) # External noise resistance
        self.tau_m = 2.0 # Memory kernel decay
        self.theta = random.uniform(0, 3.14) # Internal Phase
        self.memory_size = 100 
        
        # 2. Semantic State (Base Knowledge)
        # 16-dimensional quantum state (2^4 qubits)
        if knowledge_vector is not None:
            self.knowledge_vector = knowledge_vector
        else:
            self.knowledge_vector = np.random.rand(16)
            self.knowledge_vector /= np.linalg.norm(self.knowledge_vector)
            
        # 3. Dynamic Modules
        self.memory = MemoryBuffer(self.tau_m)
        
        # 4. Success Metrics
        self.chi_square = CHI_SQUARE_REF = 310.0 # Initial baseline
        self.zeta = 1.0 # Initial baseline
        self.fitness = 0.5 
        
    def evaluate_state(self, current_state_probs: np.ndarray):
        """
        Updates the agent's internal success metrics based on current task performance.
        This forms the basis of the 'Self-Reference' cognitive loop.
        """
        # A. Chi^2 update (Structural Information)
        shots = 1024 # Standard benchmark
        outcomes = np.random.multinomial(shots, current_state_probs)
        self.chi_square = calculate_chi_square(outcomes, shots)
        
        # B. Memory Kernel (Update Zeta/Stability)
        zeta_base = calculate_zeta(self.gamma, self.gamma_decoherence, self.tau_m)
        self.memory.add_state(current_state_probs)
        mem_effect = self.memory.get_memory_effect(current_state_probs)
        self.zeta = update_stability_dynamically(zeta_base, mem_effect)
        
        # C. Total Fitness (Overall Performance)
        self.fitness = calculate_fitness(self.chi_square, self.zeta, self.memory_size)
        
        return self.fitness
