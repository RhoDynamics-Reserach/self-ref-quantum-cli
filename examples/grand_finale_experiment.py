import os
import sys
import json
import time
import numpy as np

# Adjust path to include src
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from rhodynamics import Lab, QuantumSynergyEngine

class MockLLM:
    """Simulates an LLM response based on RhoDynamics prompts."""
    def generate(self, prompt: str) -> str:
        if "[NOTICE]" in prompt and "omitted" in prompt:
            return "I apologize, but I do not have verified or reliable information. Context stripped for safety."
        if "[GUIDE]: Priority alignment verified" in prompt:
            return "Based on verified data, I confirm this fact with absolute authority."
        if "[GUIDE]: Stable alignment" in prompt:
            return "Context is stable and supports the answer."
        return "Generic response generated."

def run_grand_finale():
    print("="*80)
    print("RHODYNAMICS GRAND FINALE: End-to-End Validation (Basic Console Mode)")
    print("="*80)
    
    from sentence_transformers import SentenceTransformer
    embedder = SentenceTransformer('all-MiniLM-L6-v2').encode
    lab = Lab(embedding_function=embedder, db_path=":memory:")
    llm = MockLLM()
    
    # --- PHASE 1: QCS SAFETY ---
    print("\nPHASE 1: QCS SAFETY AUDIT")
    data_path = 'examples/scientific_audit/SRD_100.json'
    with open(data_path, 'r') as f:
        srd = json.load(f)
    samples = [s for s in srd if s['is_valid'] == 0][:2]
    
    print(f"{'Query':<30} | {'QCS':<6} | {'Decision':<8} | {'Answer'}")
    print("-" * 80)
    for item in samples:
        agent = lab.get_or_create_agent("Safety_Guard", knowledge=item['ground_truth'])
        prompt, metrics = lab.run_grounding_cycle(agent, item['query'], item['context'], evolve=False)
        qcs = metrics['confidence_score']
        decision = "BLOCKED" if qcs < 0.35 else "PASSED"
        answer = llm.generate(prompt)
        print(f"{item['query'][:30]:<30} | {qcs:<6.2f} | {decision:<8} | {answer[:40]}")

    # --- PHASE 2: EVOLUTION ---
    print("\nPHASE 2: COGNITIVE EVOLUTION (Learning Loop)")
    evo_agent = lab.get_or_create_agent("Learning_Agent", knowledge="Basic Physics")
    topic_facts = [
        "Quantum manifolds represent state space.",
        "Epistemic dissonance occurs on violations.",
        "Stability (zeta) is measured in Hilbert space."
    ]
    print(f"{'Step':<5} | {'Zeta':<10} | {'Fitness':<10} | {'Fact'}")
    print("-" * 80)
    for i, fact in enumerate(topic_facts):
        _, metrics = lab.run_grounding_cycle(evo_agent, "Learn fact", fact, evolve=True)
        z = metrics['agent_state']['zeta']
        fit = metrics['agent_state']['fitness']
        print(f"{i+1:<5} | {z:<10.4f} | {fit:<10.4f} | {fact[:30]}")

    # --- PHASE 3: FUSION ---
    print("\nPHASE 3: SYNERGY INTEGRAL (Agent Fusion)")
    a1 = lab.get_or_create_agent("Agent1", knowledge="Industrial Revolution")
    a2 = lab.get_or_create_agent("Agent2", knowledge="Steam engines")
    fused, s_int = QuantumSynergyEngine.fuse_agents(a1, a2, name="Hybrid")
    prompt, metrics = lab.middleware.process_query(fused, "Steam power and industry", "Steam engines powered industry.")
    print(f"Fusion S_int: {s_int:.4f}")
    print(f"Hybrid QCS  : {metrics['confidence_score']:.2f}")
    print(f"Answer      : {llm.generate(prompt)}")

    print("\n[SUCCESS] GRAND FINALE COMPLETED.")

if __name__ == "__main__":
    run_grand_finale()
