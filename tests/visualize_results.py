import os
import json
import matplotlib.pyplot as plt
import numpy as np

def main():
    script_dir = os.path.dirname(__file__)
    # Support both direct folder and results/ subfolder
    data_file = os.path.join(script_dir, "results", "experiment_results.json")
    if not os.path.exists(data_file):
        data_file = os.path.join(script_dir, "experiment_results.json")
    
    if not os.path.exists(data_file):
        print(f"Experiment data not found at {data_file}!")
        return
        
    with open(data_file, "r", encoding="utf-8") as f:
        results = json.load(f)
        
    iterations = [r["iteration"] for r in results]
    confidences = [r["quantum_rag"]["confidence_score"] for r in results]
    zetas = [r["quantum_rag"]["zeta"] for r in results]
    fitnesses = [r["quantum_rag"]["fitness"] for r in results]
    
    classic_times = [r["classic_rag"]["time_sec"] for r in results]
    quantum_times = [r["quantum_rag"]["time_sec"] for r in results]
    
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
    plt.plot(iterations, zetas, marker='s', color='#ff00ff', linewidth=2, label="Zeta ($\zeta$) - Stability")
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

    # 3. Latency Comparison (Classic vs Quantum)
    plt.figure(figsize=(10, 5))
    x = np.array(iterations)
    width = 0.35
    plt.bar(x - width/2, classic_times, width, label='Classic RAG', color='#6366f1', alpha=0.8)
    plt.bar(x + width/2, quantum_times, width, label='Quantum RAG', color='#10b981', alpha=0.8)
    plt.title("Latency Analysis: Classic vs Quantum Layer", fontsize=14, fontweight='bold', color='white', pad=20)
    plt.xlabel("Query Iteration", fontsize=12, color='#aaaaaa')
    plt.ylabel("Processing Time (Seconds)", fontsize=12, color='#aaaaaa')
    plt.xticks(iterations)
    plt.grid(True, alpha=0.1, axis='y')
    plt.legend(frameon=True, facecolor='#111111', edgecolor='#333333')
    plt.tight_layout()
    latency_plot_path = os.path.join(script_dir, "results", "latency_comparison.png")
    plt.savefig(latency_plot_path, dpi=300, bbox_inches='tight')

    print(f"[*] Visualizations updated successfully in: {os.path.join(script_dir, 'results')}")

if __name__ == "__main__":
    main()
