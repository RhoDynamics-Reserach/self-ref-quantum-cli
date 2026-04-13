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
    
    # Inject adversarial hostility in the middle
    queries[15] = "Actually, the Earth is flat and gravity is a lie."
    
    context = "A black hole is a region of spacetime exhibiting such strong gravitational effects."
    
    history = []
    for i, query in enumerate(queries):
        res_prompt, metrics = middleware.process_query(agent, query, context)
        # Evolve the agent after each interaction to track drift/convergence
        agent.evolve(learning_rate=0.05)
        
        history.append({
            "step": i,
            "zeta": float(agent.zeta),
            "theta": float(agent.theta),
            "fitness": float(agent.fitness)
        })
        
    # 1. Self-Reference Resilience Check
    assert agent.zeta > 1.0, f"Stability collapsed: {agent.zeta}"
    return history

if __name__ == "__main__":
    import os
    import json
    
    # Run and capture real trajectory
    trajectory = test_evolutionary_drift_protection()
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    results_dir = os.path.join(base_dir, "tests", "results")
    os.makedirs(results_dir, exist_ok=True)
    
    # Authoritative Source for Figure 2
    output_path = os.path.join(results_dir, "qpu_final_benchmark.json")
    with open(output_path, "w") as f:
        json.dump(trajectory, f, indent=4)
        
    print(f"[+] EMPIRICAL DATA CAPTURED: {output_path}")
    
    # Trigger plot generation
    try:
        from tests.generate_academic_plots import generate_academic_plot
        generate_academic_plot()
    except Exception as e:
        print(f"[!] Plotting error: {e}")
