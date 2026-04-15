import numpy as np
from .agent_model import BaseQuantumAgent

class QuantumSynergyEngine:
    """
    Handles Multi-Agent Entanglement and Knowledge Fusion.
    Allows for combining specialized RAG agents into a single cooperative node.
    """
    
    @staticmethod
    def fuse_agents(agent_A: BaseQuantumAgent, agent_B: BaseQuantumAgent, name: str = "SynergyAgent", weight_A: float = 0.5):
        """
        Entangles two agent state vectors to produce a new superimposed quantum agent.
        Calculates the Synergy Integral (S_int) representing the constructive/destructive interference.
        
        Returns:
            Tuple[BaseQuantumAgent, float]: The newly formed Synergy Agent, and the S_int score (-1.0 to 1.0).
        """
        weight_A = max(0.0, min(1.0, weight_A))
        weight_B = 1.0 - weight_A
        
        vec_A = agent_A.knowledge_vector
        vec_B = agent_B.knowledge_vector
        
        # Ensure dimensions match
        if len(vec_A) != len(vec_B):
            raise ValueError(f"Agent dimension mismatch: {len(vec_A)} vs {len(vec_B)}")
            
        # 1. Synergy Integral ($S_{int}$) Calculus
        # Interference between the two normalized cognitive vectors
        norm_A = np.linalg.norm(vec_A)
        norm_B = np.linalg.norm(vec_B)
        
        s_int = 0.0
        if norm_A > 0 and norm_B > 0:
            # The Quantum Phase Match (Dot Product)
            # High s_int -> Constructive (Synergy)
            # Low/Negative s_int -> Destructive (Conflict)
            s_int = float(np.dot(vec_A, vec_B) / (norm_A * norm_B))
            
        # 2. Non-Linear Superposition Merging (Hadamard Fusion)
        # linear base
        linear_superposition = (weight_A * vec_A) + (weight_B * vec_B)
        
        # Non-linear entanglement term via element-wise multiplication
        # We scale its impact based on the absolute magnitude of S_int (strong interaction -> strong entanglement)
        hadamard_entanglement = vec_A * vec_B
        kappa = abs(s_int) * 0.5 # Entanglement coupling factor
        
        superposition = linear_superposition + (kappa * hadamard_entanglement)
        
        # 3. Phase Normalization & Unitary Constraint
        # Ensure resulting vector lies on the unit sphere for valid quantum probabilities
        norm = np.linalg.norm(superposition)
        if norm > 0:
            superposition = superposition / norm
        
        # Instantiate the new Synergy Agent
        synergy_agent = BaseQuantumAgent(name=name, knowledge_vector=superposition)
        
        # Blend Cognitive Parameters
        synergy_agent.zeta = (agent_A.zeta * weight_A) + (agent_B.zeta * weight_B)
        synergy_agent.tau_m = (agent_A.tau_m * weight_A) + (agent_B.tau_m * weight_B)
        synergy_agent.fitness = (agent_A.fitness * weight_A) + (agent_B.fitness * weight_B)
        
        return synergy_agent, s_int
