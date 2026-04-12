import os
import json
import numpy as np
import time
from dotenv import load_dotenv

from quantum_rag_layer.hardware_connector import QuantumHardwareConnector
from quantum_rag_layer.agent_model import BaseQuantumAgent
from quantum_rag_layer.rag_engine import QuantumRAGLayer

load_dotenv()

def generate_synthetic_scaling_dataset(num_samples=30):
    """
    Generates a scaled dataset of random simulated context vectors.
    Since we are testing the underlying mathematics, synthetic vectors
    serve to prove the manifold behavior correctly scales.
    Returns pairs of (task_vector, context_vector, expected_fitness_trend).
    """
    dataset = []
    for i in range(num_samples):
        # Generate random probability distributions (simulating LLM embeddings)
        t_vec = np.random.rand(16)
        c_vec = np.random.rand(16)
        
        # Introduce "Good" (aligned) and "Bad" (orthogonal) contexts
        if i % 3 == 0:
            c_vec = t_vec + (np.random.rand(16) * 0.1) # Aligned
        elif i % 3 == 1:
            c_vec = 1.0 - t_vec # Extremely orthogonal / mismatched
        
        t_vec /= np.linalg.norm(t_vec)
        c_vec /= np.linalg.norm(c_vec)
        
        dataset.append((t_vec, c_vec))
    return dataset

def run_hardware_benchmark():
    print("="*60)
    print(" [RHO-DYNAMICS] FINAL IBM QUANTUM HARDWARE BENCHMARK ")
    print("="*60)
    
    token = os.getenv("IBM_QUANTUM_TOKEN")
    if not token:
        print("[!] No IBM_QUANTUM_TOKEN found. Cannot run hardware benchmark.")
        return

    print("[*] Connecting to IBM Quantum Runtime...")
    try:
        # For a fast academic test, try ibmq_qasm_simulator. 
        # If queue empty, it will use real minimal backend.
        connector = QuantumHardwareConnector(api_token=token)
    except Exception as e:
        print(f"[!] Critical Error connecting to IBM: {e}")
        return

    # Create Agent
    base_state = np.random.rand(16)
    base_state /= np.linalg.norm(base_state)
    target_agent = BaseQuantumAgent("Final_QPU_Agent", knowledge_vector=base_state, measurement_executor=connector)
    rag_layer = QuantumRAGLayer()
    
    # Dataset
    num_samples = 30
    dataset = generate_synthetic_scaling_dataset(num_samples)
    print(f"[*] Generated Dataset of {num_samples} semantic scenarios.")
    print(f"[*] Backend: {connector.backend.name if connector.backend else 'Unknown'}")
    print("[*] Initiating Scaled Sequence...\n")
    
    results_list = []
    
    # We must warn the user if it's a real chip because each iteration causes a queue job.
    if connector.is_real_hardware() and "simulator" not in str(connector.backend.name).lower():
        print(">> [WARNING] Executing on REAL PHYSICAL CHIP. This might take HOURS due to queue.")
        print(">> [WARNING] Press Ctrl+C if you want to abort and use simulator fallback.")
        time.sleep(3)
        
    for i, (t_vec, c_vec) in enumerate(dataset):
        start_t = time.time()
        print(f"   [Step {i+1}/{num_samples}] Dispatching job to queue...")
        
        # This will block while running on QPU
        try:
           res = rag_layer.process_with_context(
               agent=target_agent,
               task_vector=t_vec,
               context_vector=c_vec,
               learning_rate=0.1
           )
           
           results_list.append({
               "step": i + 1,
               "qcs": res["confidence_score"],
               "zeta": res["agent_state"]["zeta"],
               "theta": res["agent_state"]["theta"],
               "gamma": res["agent_state"]["gamma"],
               "fitness": res["agent_state"]["fitness"]
           })
           
           elapsed = time.time() - start_t
           print(f"   [>] Success | Zeta: {res['agent_state']['zeta']:.3f} | Theta: {res['agent_state']['theta']:.3f} | Time: {elapsed:.1f}s")
           
        except Exception as e:
           print(f"   [!] Job Failure: {e}")
           break

    # Save outputs
    out_dir = os.path.join(os.path.dirname(__file__), "results")
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        
    out_file = os.path.join(out_dir, "qpu_final_benchmark.json")
    with open(out_file, "w") as f:
        json.dump(results_list, f, indent=4)
        
    print("\n" + "="*60)
    print(f"[*] Benchmark complete. Data exported to: {out_file}")
    print("="*60)

if __name__ == "__main__":
    run_hardware_benchmark()
