import os
import json
import matplotlib.pyplot as plt
import numpy as np

def main():
    script_dir = os.path.dirname(__file__)
    data_file = os.path.join(script_dir, "experiment_results.json")
    
    if not os.path.exists(data_file):
        print("Experiment data not found! Please run experiment_runner.py first.")
        return
        
    with open(data_file, "r", encoding="utf-8") as f:
        results = json.load(f)
        
    iterations = [r["iteration"] for r in results]
    confidences = [r["quantum_rag"]["confidence_score"] for r in results]
    zetas = [r["quantum_rag"]["zeta"] for r in results]
    fitnesses = [r["quantum_rag"]["fitness"] for r in results]
    
    plt.style.use('dark_background')
    
    # 1. Quantum Confidence Score Plot
    plt.figure(figsize=(10, 5))
    plt.plot(iterations, confidences, marker='o', color='cyan', linewidth=2, label="Quantum Confidence Score (QCS)")
    plt.fill_between(iterations, confidences, alpha=0.2, color='cyan')
    plt.title("Quantum RAG Layer: Confidence Evolution Over Queries", fontsize=14)
    plt.xlabel("Query Iteration", fontsize=12)
    plt.ylabel("Confidence (0.0 - 1.0)", fontsize=12)
    plt.ylim(0, 1.1)
    plt.xticks(iterations)
    plt.grid(True, alpha=0.3, linestyle="--")
    plt.legend()
    plt.tight_layout()
    qcs_plot_path = os.path.join(script_dir, "qcs_graph.png")
    plt.savefig(qcs_plot_path, dpi=300)
    print(f"Saved QCS graph to: {qcs_plot_path}")
    
    # 2. Agent Stability vs Fitness Plot
    plt.figure(figsize=(10, 5))
    plt.plot(iterations, zetas, marker='s', color='#ff00ff', linewidth=2, label="Zeta ($\zeta$) - Stability")
    plt.plot(iterations, fitnesses, marker='^', color='#00ff00', linewidth=2, label="Fitness ($F$) - Adaptation")
    plt.title("Agent Cognitive Evolution: Stability & Fitness", fontsize=14)
    plt.xlabel("Query Iteration", fontsize=12)
    plt.ylabel("Score Metrics", fontsize=12)
    plt.ylim(0, max(max(zetas), max(fitnesses)) * 1.5)
    plt.xticks(iterations)
    plt.grid(True, alpha=0.3, linestyle="--")
    plt.legend()
    plt.tight_layout()
    evolution_plot_path = os.path.join(script_dir, "stability_evolution_graph.png")
    plt.savefig(evolution_plot_path, dpi=300)
    print(f"Saved Evolution graph to: {evolution_plot_path}")

if __name__ == "__main__":
    main()
