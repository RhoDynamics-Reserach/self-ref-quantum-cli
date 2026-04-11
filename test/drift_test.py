import sys
import os
import json
import numpy as np

# Ensure we can import from the parent package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from quantum_rag_layer.middleware import QuantumMiddleware
from quantum_rag_layer.agent_model import BaseQuantumAgent

def mock_embedding(text):
    """Simulates a 16-dimensional embedding."""
    # Deterministic mock based on text length for test stability
    np.random.seed(len(text))
    vec = np.random.rand(16)
    return vec / np.linalg.norm(vec)

def run_drift_test():
    print("\n" + "="*80)
    print(" [DRIFT TEST] QUANTUM RAG LAYER: SEQUENTIAL EVOLUTION ANALYSIS ")
    print("="*80)
    
    # 1. Setup
    middleware = QuantumMiddleware(embedding_function=mock_embedding)
    agent = middleware.create_agent("Evolving-Scientist")
    
    # 2. Sequential Queries (Topic: Astrophysics)
    queries = [
        "What is a black hole?",
        "How do black holes form from stars?",
        "What is the event horizon?",
        "Can information escape a black hole?",
        "What is Hawking radiation?",
        "How does gravity warp time near a black hole?",
        "What happens at the singularity?",
        "Are there supermassive black holes?",
        "How do we observe them if they are black?",
        "What is a quasar?"
    ]
    
    context = "A black hole is a region of spacetime where gravity is so strong that nothing, including light, can escape. According to Hawking radiation theory, they can emit thermal energy. The event horizon marks the boundary of no return."
    
    results = []
    
    print(f"[*] Starting Evolution Cycle (Learning Rate: 0.1)")
    print(f"{'Step':<5} | {'QCS':<6} | {'Zeta':<6} | {'Fitness':<8} | {'Theta':<6} | {'Gamma':<6}")
    print("-" * 60)
    
    for i, query in enumerate(queries):
        # We increase context relevance slightly per step to simulate 'Deepening focus'
        # Or keep it steady to see if agent 'Locks in'
        res_prompt, metrics = middleware.process_query(agent, query, context)
        
        results.append({
            "step": i + 1,
            "qcs": metrics["confidence_score"],
            "zeta": agent.zeta,
            "fitness": agent.fitness,
            "theta": agent.theta,
            "gamma": agent.gamma
        })
        
        print(f"{i+1:<5} | {metrics['confidence_score']:<6.2f} | {agent.zeta:<6.2f} | {agent.fitness:<8.2f} | {agent.theta:<6.2f} | {agent.gamma:<6.2f}")

    # 3. Final Analysis
    ini_zeta = results[0]["zeta"]
    fin_zeta = results[-1]["zeta"]
    drift_protection = "STABLE" if fin_zeta >= ini_zeta * 0.9 else "DRIFTING"
    
    print("-" * 60)
    print(f"[RESULT] Final Status: {drift_protection}")
    print(f"[RESULT] Parameter Shift: Theta({results[0]['theta']:.2f} -> {results[-1]['theta']:.2f})")
    print(f"[RESULT] Intelligence Gain (Fitness): {results[0]['fitness']:.2f} -> {results[-1]['fitness']:.2f}")
    
    # Save results for visualization
    report_path = os.path.join(os.path.dirname(__file__), "results", "drift_results.json")
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w") as f:
        json.dump(results, f, indent=4)
    
    print(f"[*] Drift history saved to: {report_path}")
    print("="*80 + "\n")

if __name__ == "__main__":
    run_drift_test()
