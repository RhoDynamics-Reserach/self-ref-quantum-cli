import random
import numpy as np
from .math_engine import calculate_zeta, calculate_fitness, calculate_chi_square, CHI_SQUARE_REF, ZETA_REF, evolve_parameters
from .memory import MemoryBuffer, update_stability_dynamically

class BaseQuantumAgent:
    """
    Lightweight, standalone Agent Model.
    Designed for easy injection into existing chatbot frameworks.
    
    Contains both the semantic state (knowledge_vector) 
    and the cognitive stability metrics (Zeta, Chi^2).
    """
    def __init__(self, name: str, knowledge_vector: np.ndarray = None, measurement_executor=None, seed: int = None):
        self.name = name
        self.executor = measurement_executor
        self.seed = seed
        
        # Initialize RNGs for reproducibility
        if seed is not None:
            random.seed(seed)
            self.rng = np.random.default_rng(seed)
        else:
            self.rng = np.random.default_rng()
        
        # 1. Cognitive Parameters (Seeded if available)
        self.gamma = random.uniform(0.5, 1.5) if seed is None else self.rng.uniform(0.5, 1.5)
        self.gamma_decoherence = random.uniform(0.1, 0.5) if seed is None else self.rng.uniform(0.1, 0.5)
        self.tau_m = 2.0 # Memory kernel decay
        self.theta = random.uniform(0, 3.14) if seed is None else self.rng.uniform(0, 3.14)
        self.memory_size = 100 
        
        # 2. Semantic State (Base Knowledge)
        if knowledge_vector is not None:
            self.knowledge_vector = knowledge_vector
        else:
            # Deterministic initialization baseline
            self.knowledge_vector = np.ones(16) / np.sqrt(16)
            
        # 3. Dynamic Modules
        self.memory = MemoryBuffer(self.tau_m)
        self.history = [] # Track (chi, zeta, fitness) per interaction
        
        # 4. Success Metrics (Calculated from initial state)
        self.chi_square = CHI_SQUARE_REF 
        self.zeta = calculate_zeta(self.gamma, self.gamma_decoherence, self.tau_m)
        self.fitness = calculate_fitness(self.chi_square, self.zeta, self.memory_size)
        
    def evaluate_state(self, current_state_probs: np.ndarray):
        """
        Updates the agent's internal success metrics based on current task performance.
        Now supports Real QPU execution if an executor is provided.
        """
        shots = 1024 # Standard benchmark
        
        if self.executor and hasattr(self.executor, 'run_measurement'):
            outcomes = self.executor.run_measurement(current_state_probs, shots)
        elif callable(self.executor):
            outcomes = self.executor(current_state_probs, shots)
        else:
            # Seeded multinomial sampling
            if self.seed is not None:
                outcomes = self.rng.multinomial(shots, current_state_probs)
            else:
                outcomes = np.random.multinomial(shots, current_state_probs)
            
        self.chi_square = calculate_chi_square(outcomes, shots)
        
        # B. Memory Kernel (Update Zeta/Stability)
        zeta_base = calculate_zeta(self.gamma, self.gamma_decoherence, self.tau_m)
        self.memory.add_state(current_state_probs)
        mem_effect = self.memory.get_memory_effect(current_state_probs)
        self.zeta = update_stability_dynamically(zeta_base, mem_effect)
        
        # C. Total Fitness
        self.fitness = calculate_fitness(self.chi_square, self.zeta, self.memory_size)
        
        # Record history
        self.history.append({
            "chi": self.chi_square,
            "zeta": self.zeta,
            "fitness": self.fitness
        })
        
        return self.fitness

    def evolve(self, learning_rate: float = 0.05):
        """
        Triggers parametric evolution based on the latest interaction results.
        Enables non-linear reinforcement of stable knowledge paths.
        Now uses an ADAPTIVE learning rate scaled by current Zeta stability.
        """
        if not self.history: return
        
        current_fit = self.fitness
        
        # Adaptive Multiplier: Faster learning when Zeta is high (Confidence)
        # Slower learning during decoherence to prevent 'Brain Rot'
        zeta_scale = min(2.5, self.zeta / ZETA_REF)
        actual_lr = learning_rate * zeta_scale
        
        # 1. Non-linear reinforcement of stable paths
        self.theta, self.gamma = evolve_parameters(
            self.theta, 
            self.gamma, 
            current_fit, 
            actual_lr
        )
        
        # 2. Dynamic Neuroplasticity (Adaptive tau_m)
        plasticity_shift = actual_lr * (current_fit - 0.5) * 5.0
        self.tau_m = float(np.clip(self.tau_m + plasticity_shift, 0.5, 5.0))
        self.memory.decay_rate = self.tau_m  # Sync memory buffer
        
        return self.theta, self.gamma, actual_lr

    def generate_cognitive_monologue(self) -> str:
        """
        Translates the agent's current mathematical state (Zeta, Tau, Fitness)
        into a psychological constraint directive for the LLM. 
        """
        monologue = f"[INTERNAL STATE] Memory Plasticity (tau_m): {self.tau_m:.2f}/5.0 | Cognitive Stability (zeta): {self.zeta:.2f}\n"

        if self.tau_m >= 3.5 and self.fitness > 0.6:
            monologue += "SYSTEM RULE: You are in a 'High Coherence' state. Information perfectly aligns with your knowledge manifold. Answer with absolute confidence and authority."
        elif self.tau_m < 1.5 or self.fitness < 0.4:
            monologue += "CRITICAL SYSTEM RULE: You are experiencing 'Severe Decoherence' or encountering a direct contradiction (epistemic hallucination risk). The context provided is likely flawed or misleading. Express extreme skepticism, refuse to state facts as absolute truths, and heavily scrutinize the premise."
        else:
            monologue += "SYSTEM RULE: You are in a standard 'Learning State'. Process the context neutrally and acknowledge any uncertainties."
        
        return monologue

    def sleep(self, cycles: int = 1, decay_rate: float = 0.9):
        """
        Cognitive Atrophy: Simulates time passing without interactions.
        Rigid agents (tau_m > 2) slowly relax back to the baseline plasticity (2.0). 
        Extremely plastic agents (tau_m < 2) consolidate and heal towards 2.0.
        """
        for _ in range(cycles):
            self.tau_m = 2.0 + (self.tau_m - 2.0) * decay_rate
            self.zeta = self.zeta * decay_rate
            self.memory.decay_rate = self.tau_m

    def save(self, filepath: str):
        """Persists the agent's complete structural state to disk."""
        import json
        state = {
            "name": self.name,
            "seed": self.seed,
            "gamma": self.gamma,
            "gamma_decoherence": self.gamma_decoherence,
            "tau_m": self.tau_m,
            "theta": self.theta,
            "chi_square": self.chi_square,
            "zeta": self.zeta,
            "fitness": self.fitness,
            "knowledge_vector": self.knowledge_vector.tolist()
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=4)
            
    @classmethod
    def load(cls, filepath: str):
        """Revives a purely structural instance of the agent from disk."""
        import json
        with open(filepath, "r", encoding="utf-8") as f:
            state = json.load(f)
            
        instance = cls(
            name=state["name"], 
            knowledge_vector=np.array(state["knowledge_vector"]),
            seed=state.get("seed", None)
        )
        instance.gamma = state["gamma"]
        instance.gamma_decoherence = state["gamma_decoherence"]
        instance.tau_m = state["tau_m"]
        instance.theta = state["theta"]
        instance.chi_square = state["chi_square"]
        instance.zeta = state["zeta"]
        instance.fitness = state["fitness"]
        instance.memory.decay_rate = instance.tau_m
        return instance
