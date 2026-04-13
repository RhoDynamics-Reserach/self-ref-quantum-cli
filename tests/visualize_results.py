import os
import json
import matplotlib.pyplot as plt
import numpy as np

def main():
    script_dir = os.path.dirname(__file__)
    data_file = os.path.join(script_dir, "results", "qpu_final_benchmark.json")
    
    if not os.path.exists(data_file):
        print(f"Empirical data not found at {data_file}!")
        return
        
    with open(data_file, "r", encoding="utf-8") as f:
        results = json.load(f)
        
    iterations = [r["step"] for r in results]
    # In V4.0, 'fitness' serves as the composite Confidence Score (QCS)
    confidences = [r["fitness"] for r in results]
    zetas = [r["zeta"] for r in results]
    fitnesses = [r["fitness"] for r in results]
    
    plt.style.use('dark_background')
    
    # 1. Quantum Confidence Score Plot
    plt.figure(figsize=(10, 5))
    plt.plot(iterations, confidences, marker='o', color='#00f2ff', linewidth=2, label="Quantum Confidence Score (QCS)")
    plt.fill_between(iterations, confidences, alpha=0.15, color='#00f2ff')
    plt.title("Quantum RAG: Alignment & Confidence Evolution", fontsize=14, fontweight='bold', color='white', pad=20)
    plt.xlabel("Query Iteration", fontsize=12, color='#aaaaaa')
    plt.ylabel("Confidence (0.0 - 1.0)", fontsize=12, color='#aaaaaa')
    plt.ylim(0, 1.1)
    plt.xticks(iterations)
    plt.grid(True, alpha=0.2, linestyle="--")
    plt.legend(frameon=True, facecolor='#111111', edgecolor='#333333')
    plt.tight_layout()
    qcs_plot_path = os.path.join(script_dir, "results", "qcs_graph.png")
    plt.savefig(qcs_plot_path, dpi=300, bbox_inches='tight')
    
    # 2. Agent Stability vs Fitness Plot (Zeta & Fitness)
    plt.figure(figsize=(10, 5))
    plt.plot(iterations, zetas, marker='s', color='#ff00ff', linewidth=2, label=r"Zeta ($\zeta$) - Stability")
    plt.plot(iterations, fitnesses, marker='^', color='#00ff00', linewidth=2, label="Fitness ($F$) - Adaptation")
    plt.title("Cognitive Evolution: Stability & Learning Rate", fontsize=14, fontweight='bold', color='white', pad=20)
    plt.xlabel("Query Iteration", fontsize=12, color='#aaaaaa')
    plt.ylabel("Normalized Metrics", fontsize=12, color='#aaaaaa')
    plt.xticks(iterations)
    plt.grid(True, alpha=0.2, linestyle="--")
    plt.legend(frameon=True, facecolor='#111111', edgecolor='#333333')
    plt.tight_layout()
    evolution_plot_path = os.path.join(script_dir, "results", "stability_evolution_graph.png")
    plt.savefig(evolution_plot_path, dpi=300, bbox_inches='tight')

    print(f"[*] Visualizations updated successfully in: {os.path.join(script_dir, 'results')}")

if __name__ == "__main__":
    main()
