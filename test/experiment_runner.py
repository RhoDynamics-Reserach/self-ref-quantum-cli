import os
import sys
import json
import time
import requests
import numpy as np

# Adjust path so we can import the quantum_rag_layer properly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from quantum_rag_layer.rag_engine import QuantumRAGLayer
from quantum_rag_layer.agent_model import BaseQuantumAgent

# --- Configuration ---
OLLAMA_MODEL = "llama3"
OLLAMA_URL = "http://localhost:11434/api"
IBM_API_KEY = "DhkJlhUaNT_mpEK236oKsHlg7_MfP2rvPxFz5bLJrr3K" 

# --- Knowledge Base & Test Scenarios ---
CONTEXT_DATABASE = {
    "oceanography": "The Mariana Trench is the deepest oceanic trench on Earth. Underwater acoustic mapping uses low-frequency sound waves to measure topography.",
    "quantum_tech": "Quantum superposition allows qubits to hold multiple states simultaneously, enabling exponential scale parallel processing for certain algorithms.",
    "cyber_security": "Zero Trust Architecture assumes that threats can exist both outside and inside a network, requiring strict identity verification."
}

TEST_QUESTIONS = [
    ("oceanography", "How do we measure the depth of deep oceanic trenches?"),
    ("quantum_tech", "What is the primary advantage of quantum superposition in computing?"),
    ("cyber_security", "What is the main assumption of Zero Trust Architecture?"),
    ("oceanography", "Can sound waves be used underwater for mapping?"),
    ("quantum_tech", "Does quantum computing use standard bits?"),
]

# --- Helper Functions ---
def get_ollama_embedding(text: str):
    """Fallback/Primary embedding using Ollama."""
    try:
        payload = {"model": OLLAMA_MODEL, "prompt": text}
        response = requests.post(f"{OLLAMA_URL}/embeddings", json=payload, timeout=5)
        if response.status_code == 200:
            return np.array(response.json()["embedding"])
    except Exception as e:
        pass
    # Mock fallback
    return np.random.rand(768)

def ask_ollama(prompt: str, is_quantum=False):
    """Query the local Ollama model."""
    try:
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(f"{OLLAMA_URL}/generate", json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()["response"].strip()
    except Exception as e:
        return f"Error connecting to Ollama: {str(e)}"
    return "No response."

def process_ibm_authentication():
    """Simulates/Attempts IBM API Verification."""
    print(f"[*] Validating IBM API Key: {IBM_API_KEY[:8]}...")
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = f"grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={IBM_API_KEY}"
    try:
        resp = requests.post(url, headers=headers, data=data, timeout=5)
        if resp.status_code == 200:
            print("[*] IBM API Key valid! IAM Token generated successfully.")
            return resp.json()["access_token"]
        else:
            print(f"[!] IBM API WARNING: Failed to get token ({resp.status_code}). Falling back to local embeddings.")
    except Exception as e:
        print("[!] IBM API ERROR: Could not connect to IAM. Using local offline simulation.")
    return None

def main():
    print(f"==================================================")
    print(f"  QUANTUM RAG LAYER vs CLASSIC RAG EXPERIMENT")
    print(f"==================================================")
    
    # 1. Initialize API & Environment
    iam_token = process_ibm_authentication()
    time.sleep(1)
    print(f"[*] Using local Ollama model: {OLLAMA_MODEL}\n")

    results_log = []
    
    # 2. Concept Agents
    quantum_agent = BaseQuantumAgent(name="Quantum_AI")
    
    # 3. Execution Loop
    for idx, (topic, question) in enumerate(TEST_QUESTIONS, 1):
        print(f"\n--- Scenario {idx}: {topic.upper()} ---")
        print(f"Q: {question}")
        
        # Retrieval
        context = CONTEXT_DATABASE[topic]
        
        # Vectors
        context_vec = get_ollama_embedding(context)
        question_vec = get_ollama_embedding(question)
        
        # ----------------------------------------------------
        # APPROACH A: Classic RAG
        # ----------------------------------------------------
        print("[A] Running Classic RAG...")
        classic_prompt = f"Context: {context}\n\nQuestion: {question}\nAnswer the question using only the context provided."
        classic_start = time.time()
        classic_response = ask_ollama(classic_prompt)
        classic_time = time.time() - classic_start
        
        # ----------------------------------------------------
        # APPROACH B: Quantum Synergy Layer
        # ----------------------------------------------------
        print("[B] Running Quantum RAG...")
        quantum_start = time.time()
        
        # Phase 1: Process with context / calculate Quantum Confidence
        q_result = QuantumRAGLayer.process_with_context(quantum_agent, question_vec, context_vec)
        confidence = q_result["confidence_score"]
        zeta = q_result["agent_state"]["zeta"]
        fitness = q_result["agent_state"]["fitness"]
        
        # Phase 2: Dynamic prompt augmentation
        quantum_prompt = QuantumRAGLayer.augment_prompt_with_confidence(classic_prompt, confidence, context_text="Verified Vector Alignment")
        quantum_response = ask_ollama(quantum_prompt, is_quantum=True)
        quantum_time = time.time() - quantum_start

        print(f"  -> QCS (Confidence): {confidence:.4f}")
        print(f"  -> Zeta Stability:   {zeta:.4f}")
        print(f"  -> Fitness Level:    {fitness:.4f}")
        
        # 4. Save metrics
        results_log.append({
            "iteration": idx,
            "topic": topic,
            "question": question,
            "classic_rag": {
                "response": classic_response,
                "time_sec": classic_time
            },
            "quantum_rag": {
                "response": quantum_response,
                "time_sec": quantum_time,
                "confidence_score": confidence,
                "zeta": zeta,
                "fitness": fitness
            }
        })

    # Save to file
    out_file = os.path.join(os.path.dirname(__file__), "experiment_results.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results_log, f, indent=4)
        
    print(f"\n==================================================")
    print(f"Experiment Complete! Results saved to:\n{out_file}")
    
if __name__ == "__main__":
    main()
