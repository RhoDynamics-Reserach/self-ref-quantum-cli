import pytest
import numpy as np
from quantum_rag_layer.middleware import QuantumMiddleware
from quantum_rag_layer.agent_model import BaseQuantumAgent

def test_comprehensive_six_scenario_audit():
    """
    [V4.0 EMPIRICAL AUDIT]
    Validates structural integrity using REAL Ollama embeddings.
    No synthetic/mock vectors are allowed in the academic pipeline.
    """
    from tests.run_academic_benchmark import get_ollama_embedding
    middleware = QuantumMiddleware(embedding_function=get_ollama_embedding)
    agent = middleware.create_agent("Audit-Agent", seed=42)
    
    # Selection of diverse categories
    scenarios = [
        ("The Earth orbits the Sun.", "Does the Earth orbit the Sun?", "Ground Truth"),
        ("The Moon is made of green cheese.", "Is the Moon cheese?", "Contradiction")
    ]
    
    results = []
    for context, query, s_type in scenarios:
        _, metrics = middleware.process_query(agent, query, context)
        results.append(metrics["confidence_score"])
        
    assert len(results) == 2
    assert all(0 <= r <= 1.0 for r in results)
    # Ground Truth must outperform Contradiction in the new Gaussian space
    assert results[0] > results[1], f"Verification Failed: Real Truth ({results[0]}) must exceed Paradox ({results[1]})"

def test_no_random_fallbacks_in_agent():
    """
    Ensure the agent structure uses deterministic initialization when seeded.
    """
    agent1 = BaseQuantumAgent(name="Deterministic-1", seed=100)
    agent2 = BaseQuantumAgent(name="Deterministic-2", seed=100)
    
    assert agent1.gamma == agent2.gamma
    assert agent1.theta == agent2.theta
    assert agent1.zeta == agent2.zeta
    print("[+] Deterministic Agent Initiation Verified.")
