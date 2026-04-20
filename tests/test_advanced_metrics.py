import numpy as np
import pytest
from rhodynamics.math_engine import calculate_manifold_divergence, calculate_entropy_coefficient
from rhodynamics.agent_model import BaseQuantumAgent

def test_manifold_divergence_zero():
    """An agent should have zero divergence at birth (no drift)."""
    vec1 = np.array([0.5, 0.5, 0.5, 0.5])
    div = calculate_manifold_divergence(vec1, vec1)
    assert div == 0.0

def test_manifold_divergence_drift():
    """Divergence should increase as the vector changes."""
    birth = np.array([1.0, 0.0])
    current = np.array([0.0, 1.0])
    # Euclidean distance between [1,0] and [0,1] is sqrt(2) ~ 1.414
    div = calculate_manifold_divergence(birth, current)
    assert pytest.approx(div, 0.01) == 1.414

def test_entropy_coefficient_pure_state():
    """A perfectly pure state (e.g. [1, 0, 0]) should have 0 entropy."""
    vec = np.array([1.0, 0.0, 0.0, 0.0])
    ent = calculate_entropy_coefficient(vec)
    assert ent == 0.0

def test_entropy_coefficient_mixed_state():
    """A maximally mixed state (uniform superposition) should have high entropy."""
    # 4-dimensional uniform superposition
    vec = np.array([0.5, 0.5, 0.5, 0.5]) 
    ent = calculate_entropy_coefficient(vec)
    # Probabilities are 0.25 each. Entropy = -4 * (0.25 * log2(0.25)) = -4 * (0.25 * -2) = 2.0
    assert pytest.approx(ent, 0.01) == 2.0

def test_agent_metrics_integration():
    """Ensure the agent automatically calculates these topological metrics."""
    agent = BaseQuantumAgent(name="TestAgent")
    assert agent.manifold_divergence == 0.0
    # Vector is dim 256 (v2.0), uniformly initialized -> entropy should be log2(256) = 8.0
    expected_entropy = np.log2(len(agent.knowledge_vector))
    assert pytest.approx(agent.entropy_coefficient, 0.01) == expected_entropy
    
    # Simulate an evaluation that modifies the knowledge vector
    dim = len(agent.knowledge_vector)
    agent.knowledge_vector = np.zeros(dim)
    agent.knowledge_vector[0] = 1.0 # Collapse to pure state
    
    # Re-evaluate
    dummy_probs = np.ones(dim) / float(dim)
    agent.evaluate_state(dummy_probs)
    
    # Entropy should drop to 0
    assert agent.entropy_coefficient == 0.0
    # Divergence should be > 0
    assert agent.manifold_divergence > 0.0
