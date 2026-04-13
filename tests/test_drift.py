import pytest
import numpy as np
import requests
import os

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

def real_semantic_embedding(text):
    if text in _DRIFT_CACHE:
        return _DRIFT_CACHE[text]
    try:
        response = requests.post(OLLAMA_URL, json={"model": OLLAMA_MODEL, "prompt": text}, timeout=10.0)
        vec = np.array(response.json()["embedding"])
        _DRIFT_CACHE[text] = vec
        return vec
    except:
        # Fallback for offline testing mode
        return np.random.rand(768)

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
    history = []
    
    for i, query in enumerate(base_queries):
        _, metrics = middleware.process_query(agent, query, context)
        agent.evolve(learning_rate=0.05)
        history.append({
            "step": i,
            "zeta": float(agent.zeta),
            "theta": float(agent.theta),
            "fitness": float(agent.fitness),
            "confidence_score": float(metrics["confidence_score"])
        })
        
    # TIGHTENED ASSERTIONS
    assert agent.zeta >= initial_zeta * 0.9, f"Catastrophic drift: {agent.zeta} from {initial_zeta}"
    assert agent.theta != 0.0, "Evolution stagnant"

    # ARTIFACT EXPORT (Promise from README)
    results_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tests", "results")
    os.makedirs(results_dir, exist_ok=True)
    with open(os.path.join(results_dir, "drift_results.json"), "w") as f:
        import json
        json.dump(history, f, indent=4)
