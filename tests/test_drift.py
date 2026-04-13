import pytest
import numpy as np
import requests

from quantum_rag_layer.middleware import QuantumMiddleware

OLLAMA_URL = "http://localhost:11434/api/embeddings"
OLLAMA_MODEL = "llama3"
_DRIFT_CACHE = {}

def check_ollama():
    try:
        response = requests.post(OLLAMA_URL, json={"model": OLLAMA_MODEL, "prompt": "test"}, timeout=1.0)
        return response.status_code == 200
    except:
        return False

@pytest.mark.ollama
@pytest.mark.skipif(not check_ollama(), reason="Ollama service ('llama3') unreachable")
def test_evolutionary_drift_protection():
    """
    Asserts that the framework actively prevents RAG drift across iterations.
    Uses real LLM embeddings for authentic manifold noise.
    """
    middleware = QuantumMiddleware(embedding_function=real_semantic_embedding)
    agent = middleware.create_agent("Evolving-Scientist", seed=100)
    
    base_queries = ["What is a black hole?"] * 10
    context = "A black hole is a region of spacetime exhibiting such strong gravitational effects."
    
    initial_zeta = agent.zeta
    
    for i, query in enumerate(base_queries):
        middleware.process_query(agent, query, context)
        agent.evolve(learning_rate=0.05)
        
    # TIGHTENED ASSERTIONS
    # 1. Self-Reference Resilience Check: Should not collapse below 90% of initiation
    assert agent.zeta >= initial_zeta * 0.9, f"Catastrophic drift: {agent.zeta} from {initial_zeta}"
    # 2. Convergence Check: Agent must physically evolve
    assert agent.theta != 0.0, "Evolution stagnant"
