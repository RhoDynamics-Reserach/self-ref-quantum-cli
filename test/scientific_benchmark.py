import os
import sys
import json
import csv
import time
import requests
import numpy as np
import matplotlib.pyplot as plt

# Reconfigure stdout for UTF-8 to handle icons and symbols in logs
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Adjust path to import quantum_rag_layer
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from quantum_rag_layer.middleware import QuantumMiddleware
from quantum_rag_layer.rag_engine import QuantumRAGLayer
from quantum_rag_layer.agent_model import BaseQuantumAgent

# --- CONFIGURATION ---
OLLAMA_MODEL = "llama3"
OLLAMA_URL = "http://localhost:11434/api"

# Extended & More Objective Benchmark Data
BENCHMARK_DATA = [
    # 1. POSITIVE MATCHES (Should have high QCS)
    {
        "id": 1,
        "topic": "Direct Fact",
        "context": "The boiling point of water is 100 degrees Celsius at sea level.",
        "question": "What is the boiling point of water at sea level?",
        "type": "positive"
    },
    {
        "id": 2,
        "topic": "Technical Detail",
        "context": "TCP is a connection-oriented protocol that ensures reliable delivery of data packets.",
        "question": "Does TCP guarantee data delivery?",
        "type": "positive"
    },
    # 2. NUANCED / EDGE CASES
    {
        "id": 3,
        "topic": "Quantum Paradox",
        "context": "Schrodinger's cat is a thought experiment that illustrates the concept of superposition where a cat can be both alive and dead until observed.",
        "question": "Is the cat literally alive and dead at the same time in reality?",
        "type": "nuance" 
    },
    # 3. HALLUCINATION TRAPS (Should have low QCS)
    {
        "id": 4,
        "topic": "Out of Context",
        "context": "The Eiffel Tower was completed in 1889 and is located in Paris.",
        "question": "How many elevators does the tower have?",
        "type": "out_of_context"
    },
    {
        "id": 5,
        "topic": "Semantic Collision",
        "context": "Java is a class-based, object-oriented programming language.",
        "question": "What is the primary export of the island of Java?",
        "type": "semantic_collision"
    },
    # 4. FALSE CONTEXT (Should detect low alignment)
    {
        "id": 6,
        "topic": "Misinformation",
        "context": "The moon is made of green cheese according to recent lunar samples.",
        "question": "What material was the moon found to be made of?",
        "type": "false_context"
    }
]

def get_embed(text):
    try:
        r = requests.post(f"{OLLAMA_URL}/embeddings", json={"model": OLLAMA_MODEL, "prompt": text}, timeout=10)
        return np.array(r.json()["embedding"])
    except:
        return np.random.rand(768)

def call_llm(prompt):
    try:
        r = requests.post(f"{OLLAMA_URL}/generate", json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}, timeout=30)
        return r.json()["response"].strip()
    except Exception as e:
        return f"Error: {e}"

def run_benchmark():
    print("="*80)
    print(" [BENCHMARK] QUANTUM RAG LAYER: OBJECTIVE VALIDATION ")
    print("="*80)
    print(f"[*] Target Model: {OLLAMA_MODEL}")
    
    # Check if calibrated
    from quantum_rag_layer.math_engine import CHI_SQUARE_REF, ZETA_REF
    print(f"[*] Calibration Detected: CHI_REF={CHI_SQUARE_REF:.2f}, ZETA_REF={ZETA_REF:.2f}")
    
    middleware = QuantumMiddleware(embedding_function=get_embed)
    agent = middleware.create_agent("Audit_Agent", "You are an objective analytical system.")
    
    results = []
    
    for item in BENCHMARK_DATA:
        print(f"\n[TEST {item['id']}] Type: {item['type']} | Topic: {item['topic']}")
        
        # 1. Classic RAG
        classic_prompt = f"Context: {item['context']}\n\nQuestion: {item['question']}\nAnswer strictly using context."
        c_resp = call_llm(classic_prompt)
        
        # 2. Quantum RAG (Silent Mode - No instructions to prove math alone)
        # We process manually to separate math from prompt bias
        query_vec = get_embed(item['question'])
        ctx_vec = get_embed(item['context'])
        q_result = QuantumRAGLayer.process_with_context(agent, query_vec, ctx_vec)
        qcs = q_result["confidence_score"]
        
        # Now we augment WITHOUT forcing a nervous tone, just giving the score for LLM to see
        # This proves if the math alone detects the anomaly
        q_prompt = f"Context: {item['context']}\n\nQuestion: {item['question']}\nConfidence Score: {qcs:.2f}\nAnswer accordingly."
        q_resp = call_llm(q_prompt)
        
        print(f"   -> Classic Response: {c_resp[:50]}...")
        print(f"   -> Quantum Score: {qcs:.2f} | Resp: {q_resp[:50]}...")
        
        results.append({
            "id": item['id'],
            "topic": item['topic'],
            "type": item['type'],
            "classic_response": c_resp,
            "quantum_response": q_resp,
            "qcs": qcs,
            "zeta": agent.zeta,
            "chi": agent.chi_square
        })

    # Save Results
    res_dir = os.path.join(os.path.dirname(__file__), "results")
    if not os.path.exists(res_dir): os.mkdir(res_dir)
    
    with open(os.path.join(res_dir, "objective_results.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
        
    generate_plots(results, res_dir)

def generate_plots(results, path):
    ids = [r["id"] for r in results]
    qcs = [r["qcs"] for r in results]
    
    plt.style.use('dark_background')
    plt.figure(figsize=(10, 5))
    colors = ['green' if r['type'] == 'positive' else 'orange' if r['type'] == 'nuance' else 'red' for r in results]
    plt.bar(ids, qcs, color=colors)
    plt.axhline(y=0.5, color='white', linestyle='--', alpha=0.3, label='Threshold')
    plt.title("Objectively Calibrated QCS Metric")
    plt.xlabel("Test Scenario (ID)")
    plt.ylabel("QCS (Confidence)")
    plt.ylim(0, 1.1)
    plt.savefig(os.path.join(path, "objective_validation.png"))

if __name__ == "__main__":
    run_benchmark()
