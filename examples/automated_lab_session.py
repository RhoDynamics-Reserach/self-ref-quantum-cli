import os
import sys

# Ensure the 'src' directory is in PYTHONPATH for local execution
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC_PATH = os.path.join(REPO_ROOT, "src")
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

import rhodynamics as rho
import numpy as np

# 1. Mock Embedding Function
def mock_embed(text: str) -> np.ndarray:
    """Mock embedding for local demonstration."""
    # Using 384-D for a more realistic mock representation
    return np.random.rand(384)

def run_experiment():
    print("[*] Initializing RhoDynamics Laboratory...")
    
    # 2. Setup the Lab (Automatically handles DB and Adapters)
    lab = rho.Lab(embedding_function=mock_embed)
    
    # 3. Create or Load an Agent
    agent = lab.get_or_create_agent(
        name="SDK_Demo_Agent", 
        knowledge="Expert in SDK integrations and python automation."
    )
    print(f"\n[Agent] {agent.name} | Initial Zeta: {agent.zeta:.3f} | Divergence: {agent.manifold_divergence:.3f}")
    
    # 4. Run multiple grounding cycles (Evolution)
    print("\n[*] Running 5 Evolutionary Grounding Cycles...")
    for i in range(5):
        query = f"How robust is integration method {i}?"
        context = f"Method {i} is highly robust."
        
        prompt, metrics = lab.run_grounding_cycle(
            agent=agent,
            user_query=query,
            retrieved_context=context,
            evolve=True
        )
        print(f"   Cycle {i+1} | QCS: {metrics['confidence_score']:.3f} | Zeta: {agent.zeta:.3f}")
        
    # 5. Generate Academic Telemetry Plot
    print("\n[*] Generating Telemetry Plot...")
    plot_path = os.path.join(REPO_ROOT, "docs", f"{agent.name}_evolution.png")
    rho.AgentTelemetry.plot_evolution(agent, output_path=plot_path)
    
    print(f"\n[OK] Experiment Complete! Plot saved to: {plot_path}")

if __name__ == '__main__':
    run_experiment()
