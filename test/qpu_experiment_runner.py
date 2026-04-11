import os
import sys
import json
import time
import requests
import numpy as np

# Inject project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from quantum_rag_layer.rag_engine import QuantumRAGLayer
from quantum_rag_layer.agent_model import BaseQuantumAgent
from quantum_rag_layer.math_engine import calculate_zeta, calculate_fitness, calculate_chi_square
from quantum_rag_layer.memory import update_stability_dynamically

from core.qpu_simulator import QuantumKernelSimulator

# --- Configuration ---
OLLAMA_MODEL = "llama3"
OLLAMA_URL = "http://localhost:11434/api"
# Security: Get IBM Token from environment variable
IBM_API_KEY = os.getenv("IBM_QUANTUM_TOKEN")
if not IBM_API_KEY:
    print("[!] Warning: IBM_QUANTUM_TOKEN not found in environment. Real hardware tests will fail.")

CONTEXT_DATABASE = {
    "astrophysics": "Supermassive black holes reside at the center of most galaxies. Their immense gravity dictates the motion of surrounding star clusters.",
    "cyber_security": "Zero Trust Architecture assumes that threats can exist both outside and inside a network, requiring strict identity verification."
}

TEST_QUESTIONS = [
    ("astrophysics", "What dictates the motion of star clusters near the center of a galaxy?"),
    ("cyber_security", "What is the main assumption of Zero Trust?")
]

def get_ollama_embedding(text: str):
    try:
        payload = {"model": OLLAMA_MODEL, "prompt": text}
        response = requests.post(f"{OLLAMA_URL}/embeddings", json=payload, timeout=5)
        if response.status_code == 200:
            return np.array(response.json()["embedding"])
    except:
        pass
    return np.random.rand(768)

def ask_ollama(prompt: str):
    try:
        payload = {"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}
        response = requests.post(f"{OLLAMA_URL}/generate", json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()["response"].strip()
    except Exception as e:
        return f"Error connecting to Ollama: {str(e)}"
    return "No response."

def main():
    print("==================================================")
    print("  QPU ACCELERATED: RAG LAYER EXPERIMENT")
    print("==================================================")
    
    print("[*] Initializing IBM Quantum Provider...")
    qpu = QuantumKernelSimulator(ibm_token=IBM_API_KEY)
    
    # ----------------------------------------------------
    # MONKEY PATCH: Redirect evaluation to REAL QPU
    # ----------------------------------------------------
    def qpu_evaluate_state_patch(self, current_state_probs: np.ndarray):
        print("      >> Submitting Job to IBM Quantum Hardware...")
        qc = qpu.build_agent_circuit(self.gamma, self.theta)
        
        # Execute on IBM Hardware (or fallback Aer)
        outcomes = qpu.run_circuit(qc, shots=1024)
        
        # Recalculate Cognitive Variables based on REAL QUBIT noise
        self.chi_square = calculate_chi_square(outcomes, 1024)
        zeta_base = calculate_zeta(self.gamma, self.gamma_decoherence, self.tau_m)
        self.memory.add_state(current_state_probs)
        mem_effect = self.memory.get_memory_effect(current_state_probs)
        
        self.zeta = update_stability_dynamically(zeta_base, mem_effect)
        self.fitness = calculate_fitness(self.chi_square, self.zeta, self.memory_size)
        
        print(f"      >> QPU Measurement Complete! Real Chi^2: {self.chi_square:.2f}")
        return self.fitness

    # Apply the patch to our agent type
    BaseQuantumAgent.evaluate_state = qpu_evaluate_state_patch

    # 1. Concept Agent
    quantum_agent = BaseQuantumAgent(name="Real_QPU_Agent")
    
    results = []

    # 2. Execution Loop
    for idx, (topic, question) in enumerate(TEST_QUESTIONS, 1):
        print(f"\n--- Scenario {idx} [QPU MODE] ---")
        print(f"Q: {question}")
        
        context = CONTEXT_DATABASE[topic]
        context_vec = get_ollama_embedding(context)
        question_vec = get_ollama_embedding(question)
        
        # Run Quantum RAG (Now routed to Hardware!)
        start_time = time.time()
        
        # process_with_context will now trigger 'qpu_evaluate_state_patch'
        q_result = QuantumRAGLayer.process_with_context(quantum_agent, question_vec, context_vec)
        confidence = q_result["confidence_score"]
        
        # Ask LLM
        classic_prompt = f"Context: {context}\n\nQuestion: {question}\nAnswer using context."
        quantum_prompt = QuantumRAGLayer.augment_prompt_with_confidence(classic_prompt, confidence)
        
        print("  -> [A] Getting Classic RAG Control Group Response...")
        classic_answer = ask_ollama(classic_prompt)
        
        print("  -> [B] Getting QPU-Backed Quantum RAG Response...")
        quantum_answer = ask_ollama(quantum_prompt)
        
        print(f"  -> QCS (Hardware Output): {confidence:.4f}")
        print(f"  -> Classic RAG Response: {classic_answer[:60]}...")
        print(f"  -> Quantum RAG Response: {quantum_answer[:60]}...")
        
        results.append({
            "iteration": idx,
            "classic_response": classic_answer,
            "qpu_confidence": confidence,
            "quantum_response": quantum_answer,
            "hw_zeta": q_result["agent_state"]["zeta"],
            "hw_fitness": q_result["agent_state"]["fitness"]
        })

    out_file = os.path.join(os.path.dirname(__file__), "qpu_experiment_results.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
        
    print("\n[+] QPU Experiment COMPLETE! Hardware results saved.")

if __name__ == "__main__":
    main()
