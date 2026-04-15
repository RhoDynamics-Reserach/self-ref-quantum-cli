import pytest
import numpy as np

from rhodynamics import BaseQuantumAgent, QuantumSynergyEngine

def test_quantum_agent_entanglement():
    """
    Tests if two distinct quantum agents can be fused mathematically
    and normalized correctly back into a quantum-like state vector.
    """
    agent_A = BaseQuantumAgent(name="LegalBot", seed=42)
    agent_B = BaseQuantumAgent(name="FinancialBot", seed=100)
    
    # Intentionally orthogonal/different bases
    agent_A.knowledge_vector = np.array([1.0, 0.0, 0.0, 0.0])
    agent_B.knowledge_vector = np.array([0.0, 1.0, 0.0, 0.0])
    
    # Entangle with 50/50 superposition
    synergy_agent, s_int = QuantumSynergyEngine.fuse_agents(agent_A, agent_B, weight_A=0.5)
    
    # Assess S_int logic (completely orthogonal vectors -> dot product 0)
    assert np.isclose(s_int, 0.0)
    
    # Assert resulting vector is normalized correctly (sqrt(0.5) for each)
    expected_val = np.sqrt(0.5)
    
    assert np.isclose(synergy_agent.knowledge_vector[0], expected_val, atol=1e-3)
    assert np.isclose(synergy_agent.knowledge_vector[1], expected_val, atol=1e-3)
    assert np.isclose(np.linalg.norm(synergy_agent.knowledge_vector), 1.0)
    
    # Assert parameters blended
    assert synergy_agent.name == "SynergyAgent"
    assert synergy_agent.zeta > 0

def test_dynamic_neuroplasticity():
    """
    Tests if the agent's memory decay kernel (tau_m) adapts based on fitness.
    """
    agent = BaseQuantumAgent(name="AdaptiveBot", seed=42)
    initial_tau = agent.tau_m
    
    # Force high fitness to test Memory Consolidation (increase in tau_m)
    agent.fitness = 0.9  # High fitness
    agent.history.append({"chi": 1.0, "zeta": 1.0, "fitness": agent.fitness})
    agent.evolve(learning_rate=0.1)
    
    assert agent.tau_m > initial_tau, "High fitness should increase tau_m (consolidation)"
    
    # Force low fitness to test Plasticity/Forgetting (decrease in tau_m)
    mid_tau = agent.tau_m
    agent.fitness = 0.1  # Low fitness (contradiction)
    agent.evolve(learning_rate=0.2)
    
    assert agent.tau_m < mid_tau, "Low fitness should decrease tau_m (forgetting)"
