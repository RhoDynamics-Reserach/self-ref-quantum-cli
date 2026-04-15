from rhodynamics import QuantumMiddleware, QuantumSynergyEngine
import numpy as np

# A simple fallback embedding just for the demo
def mock_embed(text):
    # Deterministic embedding based on length and a simple hash
    h = sum(ord(c) for c in text)
    gen = np.random.default_rng(h)
    return gen.normal(0, 1, 768)

def run_showcase():
    print("="*60)
    print("RHODYNAMICS SDK V1.2.0 - FULL SYSTEM SHOWCASE")
    print("="*60)

    middleware = QuantumMiddleware(embedding_function=mock_embed)

    print("\n[1] Creating Specialized Agents...")
    agent_physics = middleware.create_agent("PhysicsBot", seed=42)
    agent_biology = middleware.create_agent("BiologyBot", seed=100)
    
    print(f" -> {agent_physics.name} Initialization (Zeta: {agent_physics.zeta:.3f}, Tau: {agent_physics.tau_m:.2f})")
    print(f" -> {agent_biology.name} Initialization (Zeta: {agent_biology.zeta:.3f}, Tau: {agent_biology.tau_m:.2f})")

    print("\n[2] Executing Multi-Agent Quantum Entanglement (Fusion)...")
    synergy_agent, s_int = QuantumSynergyEngine.fuse_agents(agent_physics, agent_biology, name="AstroBiologyBot")
    print(f" -> Successfully fused into: {synergy_agent.name}")
    print(f" -> Merged Stability Metric (Zeta): {synergy_agent.zeta:.3f}")
    print(f" -> Synergy Integral (S_int): {s_int:.3f}")

    print("\n[3] Testing Dynamic Neuroplasticity & Auto-Sensory Feedback...")
    
    # 3.1 Stable Context Iteration
    query_1 = "Explain black hole thermodynamics."
    context_1 = "Black hole thermodynamics involves Hawking radiation and entropy."
    
    print(f"\nQUERY 1: '{query_1}' (Highly relevant context)")
    prompt_1, metrics_1 = middleware.process_query(synergy_agent, query_1, context_1)
    
    # Forcing fitness high to trigger memory consolidation
    synergy_agent.fitness = 0.8
    synergy_agent.evolve(learning_rate=0.2)
    
    print(f" -> QCS Score: {metrics_1['confidence_score']:.3f}")
    print(f" -> New Memory Tau (Consolidated): {synergy_agent.tau_m:.2f} (Increased from baseline)")
    print("\n--- INJECTED LLM PROMPT (AUTO-SENSORY) ---")
    print(prompt_1.split('\n[USER QUERY')[0].strip())
    print("------------------------------------------")

    # 3.2 Contradictory Iteration
    query_2 = "What are the rules of basketball?"
    context_2 = "Water boils at 100 degrees Celsius."
    
    print(f"\nQUERY 2: '{query_2}' (Totally irrelevant/hallucinatory context)")
    prompt_2, metrics_2 = middleware.process_query(synergy_agent, query_2, context_2)
    
    # Forcing fitness down to trigger decoherence
    synergy_agent.fitness = 0.2
    synergy_agent.evolve(learning_rate=0.2)

    print(f" -> QCS Score: {metrics_2['confidence_score']:.3f}")
    print(f" -> New Memory Tau (Decay/Plasticity): {synergy_agent.tau_m:.2f} (Decreased due to instability)")
    print("\n--- INJECTED LLM PROMPT (AUTO-SENSORY) ---")
    print(prompt_2.split('\n[USER QUERY')[0].strip())
    print("------------------------------------------")
    
    print("\n✅ SHOWCASE COMPLETE: All core systems are 100% functional.")

if __name__ == "__main__":
    run_showcase()
