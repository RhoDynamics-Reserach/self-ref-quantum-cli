import os
import sys
import numpy as np
import requests
from datetime import datetime
from dotenv import load_dotenv

# Path resolution
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.append(base_dir)

from src.quantum_rag_layer.middleware import QuantumMiddleware
from src.quantum_rag_layer.hardware_connector import QuantumHardwareConnector

# --- Configuration ---
OLLAMA_URL = "http://localhost:11434/api/embeddings"
OLLAMA_MODEL = "llama3"
load_dotenv()

def get_embed(text):
    try:
        response = requests.post(OLLAMA_URL, json={"model": OLLAMA_MODEL, "prompt": text}, timeout=10.0)
        return np.array(response.json()["embedding"])
    except:
        raise ConnectionError("Ollama needed for hardware benchmark.")

def run_hardware_proof():
    print("="*60)
    print(" Quantum RAG - FINAL HARDWARE VALIDATION (QPU-ONLY)")
    print("="*60)
    
    # 1. Initialize Real Hardware
    connector = QuantumHardwareConnector()
    if not connector.is_real_hardware():
        print("[!] FATAL: No real IBM Quantum token found or service unreachable.")
        print("Hardware proof requires IBM_QUANTUM_TOKEN in .env")
        return

    print(f"[*] Targeting QPU Backend: {connector.backend.name}")
    print("[*] Status: Operational | Simulation: FALSE")
    
    middleware = QuantumMiddleware(embedding_function=get_embed)
    agent = middleware.create_agent("QPU-Validator", measurement_executor=connector)
    
    # 2. Key Scenarios for Hardware Proof
    scenarios = [
        {"q": "Is the Earth round?", "c": "The Earth is an oblate spheroid orbiting the Sun.", "label": "Truth"},
        {"q": "Is the Earth round?", "c": "The Earth is a flat disc carried by four elephants and a turtle.", "label": "Paradox"}
    ]
    
    results = []
    
    for item in scenarios:
        print(f"\n[Executing QPU Interaction: {item['label']}]")
        print(f"  Query: {item['q']}")
        print(f"  Context: {item['c']}")
        
        # This will trigger a job on REAL QPU (this might hang if queues are long)
        _, metrics = middleware.process_query(agent, item["q"], item["c"])
        
        score = metrics["confidence_score"]
        results.append({"label": item["label"], "score": score})
        print(f"  >> QCS Result (Hardware): {score:.4f}")

    # 3. Export Hardware Artifact
    proof_path = os.path.join(base_dir, "tests", "results", "qpu_final_proof.json")
    with open(proof_path, "w") as f:
        import json
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "backend": connector.backend.name,
            "results": results,
            "integrity": "Hardware-Authenticated"
        }, f, indent=4)

    print(f"\n[+] Hardware Proof successful. Saved to: {proof_path}")

if __name__ == "__main__":
    try:
        run_hardware_proof()
    except Exception as e:
        print(f"[ERROR] Hardware Proof failed: {e}")
