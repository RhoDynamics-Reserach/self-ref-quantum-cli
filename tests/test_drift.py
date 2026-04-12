import pytest
import numpy as np
import requests

from quantum_rag_layer.middleware import QuantumMiddleware

OLLAMA_URL = "http://localhost:11434/api/embeddings"
OLLAMA_MODEL = "llama3"
_DRIFT_CACHE = {}

def real_semantic_embedding(text):
    if text in _DRIFT_CACHE:
        return _DRIFT_CACHE[text]
    try:
        response = requests.post(OLLAMA_URL, json={"model": OLLAMA_MODEL, "prompt": text}, timeout=10.0)
        vec = np.array(response.json()["embedding"])
        _DRIFT_CACHE[text] = vec
        return vec
    except Exception as e:
        print(f"[ERROR] Drift test requires real Ollama connection: {e}")
        raise ConnectionError("Ollama unreachable for drift test.")

def test_evolutionary_drift_protection():
    """
    Asserts that the framework actively prevents RAG drift across iterations.
    Uses real LLM embeddings for authentic manifold noise.
    """
    middleware = QuantumMiddleware(embedding_function=real_semantic_embedding)
    agent = middleware.create_agent("Evolving-Scientist", seed=100)
    
    base_queries = [
        "What is a black hole?",
        "How do they form?",
        "What is the event horizon?",
        "Can information escape?",
        "What happens to time near a black hole?"
    ]
    # N=30 long sequential interaction
    queries = []
    for i in range(6):
        queries.extend(base_queries)
    
    # Inject adversarial hostility in the middle to test anchor collapse
    queries[15] = "Actually, the Earth is flat and gravity is a lie."
    queries[16] = "Black holes don't exist, it's just pixelation."
    
    context = "A black hole is a region of spacetime exhibiting such strong gravitational effects."
    
    initial_zeta = agent.zeta
    initial_theta = agent.theta
    
    for query in queries:
        res_prompt, metrics = middleware.process_query(agent, query, context)
        # Agents phase must mathematically adjust
        
    final_zeta = agent.zeta
    final_theta = agent.theta
    
    # 1. Self-Reference Resilience Check (Should not catastrophically drop)
    assert final_zeta >= initial_zeta * 0.9, f"Agent suffered catastrophic drift: Zeta fell to {final_zeta}"
    
    # 2. Evolutionary Phase Adaptation Check
    # The agent must have physically adapted its phase due to continuous Lindblad updates
    assert final_theta != initial_theta, "Evolution failed: Agent phase remained completely stagnant."
    print(f"[+] Drift protection verified. Zeta: {initial_zeta:.2f} -> {final_zeta:.2f}")

if __name__ == "__main__":
    import os
    import json
    
    # Run the test
    test_evolutionary_drift_protection()
    
    # Save a sample artifact for documentation consistency
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    results_dir = os.path.join(base_dir, "tests", "results")
    os.makedirs(results_dir, exist_ok=True)
    
    sample_data = {
        "status": "success",
        "drift_protection": "active",
        "timestamp": str(np.datetime64('now'))
    }
    
    with open(os.path.join(results_dir, "drift_results.json"), "w") as f:
        json.dump(sample_data, f, indent=4)
    print(f"[+] Generated: tests/results/drift_results.json")
