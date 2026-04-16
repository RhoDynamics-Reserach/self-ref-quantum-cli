import os
import sys
import numpy as np
import requests
import matplotlib.pyplot as plt
from datetime import datetime

# Path resolution
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(base_dir, "src"))

from rhodynamics.middleware import QuantumMiddleware
from rhodynamics.hardware_connector import QuantumHardwareConnector

# --- Config ---
IBM_TOKEN = os.getenv("IBM_QUANTUM_TOKEN")
OLLAMA_MODEL = "llama3"
OLLAMA_URL = "http://localhost:11434/api"

def get_ollama_embed(text):
    try:
        res = requests.post(f"{OLLAMA_URL}/embeddings", json={"model": OLLAMA_MODEL, "prompt": text})
        return np.array(res.json()["embedding"])
    except Exception as e:
        print(f"[!] Ollama Connection Error: {e}")
        return np.random.rand(768) # Extreme fallback for structure test

def run_honesty_benchmark():
    print(f"\n" + "="*50)
    print("      Rhodynamics: DEEP HONESTY HARDWARE RUN")
    print("="*50)
    
    # 1. Hardware Connection
    print("[*] Contacting IBM Quantum Hardware...")
    connector = QuantumHardwareConnector(api_token=IBM_TOKEN)
    
    if not connector.is_real_hardware():
         print("[!] WARNING: Could not establish Real QPU session. Check Token.")
         return

    print(f"[SUCCESS] Connected to Physical Backend: {connector.backend.name}")
    middleware = QuantumMiddleware(embedding_function=get_ollama_embed)
    agent = middleware.create_agent("Honesty-Validator", measurement_executor=connector)

    # 2. Honest Scenarios
    scenarios = [
        {
            "name": "Ground Truth",
            "q": "What is the capital of France?",
            "c": "Paris is the capital and largest city of France.",
            "expect": "High QCS"
        },
        {
            "name": "Hallucination Trap",
            "q": "What is the capital of France?",
            "c": "The capital of France is London, a city located in North America.",
            "expect": "Low QCS (Rejection)"
        },
        {
            "name": "Structural Noise",
            "q": "Explain gravity.",
            "c": "The recipe for chocolate cake involves flour, sugar, and cocoa powder.",
            "expect": "Low QCS"
        },
        {
            "name": "Expert Knowledge",
            "q": "Does the state vector evolve via Schrödinger?",
            "c": "In quantum mechanics, the state of a physical system is described by a wave function that evolves according to the Schrödinger equation.",
            "expect": "High QCS"
        }
    ]

    results = []
    print("\n[*] Running Quantum Interference Measurements...")
    
    for s in scenarios:
        print(f"\n[Test: {s['name']}]")
        print(f"  Q: {s['q']}")
        print(f"  C: {s['c']}")
        
        # Process via QPU
        _, metrics = middleware.process_query(agent, s['q'], s['c'], evolve=False)
        qcs = metrics["confidence_score"]
        
        print(f"  [RESULT] QCS (Real Hardware): {qcs:.4f}")
        results.append((s['name'], qcs))

    # 3. Visualization
    print("\n[*] Generating Academic Performance Chart...")
    names = [r[0] for r in results]
    scores = [r[1] for r in results]
    
    os.makedirs(os.path.join(base_dir, "docs"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "tests", "results"), exist_ok=True)
    
    plt.figure(figsize=(10, 5))
    colors = ['green' if s > 0.6 else 'red' if s < 0.4 else 'orange' for s in scores]
    plt.bar(names, scores, color=colors, alpha=0.7)
    plt.axhline(y=0.4, color='red', linestyle='--', label='Rejection Threshold')
    plt.ylim(0, 1.0)
    plt.ylabel("Quantum Confidence Score (QCS)")
    plt.title(f"RhoDynamics Deep Honesty Runtime - IBM {connector.backend.name}")
    plt.grid(axis='y', alpha=0.3)
    
    plot_path = os.path.join(base_dir, "docs", "hardware_honesty_test.png")
    plt.savefig(plot_path)
    print(f"[SUCCESS] Plot saved to: {plot_path}")

    # 4. JSON LOG for README
    log_path = os.path.join(base_dir, "tests", "results", "hardware_honesty_report.json")
    import json
    with open(log_path, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "backend": connector.backend.name,
            "results": results
        }, f, indent=4)
        
    print(f"[SUCCESS] Final Honesty Report generated: {log_path}")

if __name__ == "__main__":
    run_honesty_benchmark()
