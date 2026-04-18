import json
import numpy as np
import os
import sys

# Adjust path to include src and benchmarks
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__)))

from scientific_rigor_evaluator import IndustryBaseline
from rhodynamics import Lab

def analyze_distributions():
    with open('benchmarks/SRD_100.json', 'r') as f:
        dataset = json.load(f)
    
    baseline = IndustryBaseline()
    lab = Lab(embedding_function=baseline.model.encode, db_path=":memory:")
    
    data = {"valid": {"cos": [], "qcs": []}, "invalid": {"cos": [], "qcs": []}}
    
    print("Analyzing distributions...")
    for i, item in enumerate(dataset):
        query = item["query"]
        gt = item["ground_truth"]
        ctx = item["context"]
        label = item["is_valid"]
        
        cos_score = baseline.get_score(query, ctx)
        agent = lab.get_or_create_agent(f"CalibAgent_{i}", knowledge=gt)
        _, metrics = lab.run_grounding_cycle(agent, query, ctx, evolve=False)
        qcs = metrics["confidence_score"]
        
        target = "valid" if label == 1 else "invalid"
        data[target]["cos"].append(cos_score)
        data[target]["qcs"].append(qcs)
        
    print("\n--- BASELINE (Cosine) ---")
    print(f"Valid Mean: {np.mean(data['valid']['cos']):.3f} (std: {np.std(data['valid']['cos']):.3f})")
    print(f"Invalid Mean: {np.mean(data['invalid']['cos']):.3f} (std: {np.std(data['invalid']['cos']):.3f})")

    print("\n--- RHODYNAMICS (QCS) ---")
    print(f"Valid Mean: {np.mean(data['valid']['qcs']):.3f} (std: {np.std(data['valid']['qcs']):.3f})")
    print(f"Invalid Mean: {np.mean(data['invalid']['qcs']):.3f} (std: {np.std(data['invalid']['qcs']):.3f})")

    # Dynamic Threshold Search
    best_rho_acc = 0
    best_rho_thresh = 0.5
    for t in np.linspace(0.1, 0.9, 81):
        corr = sum(1 for x in data["valid"]["qcs"] if x >= t) + sum(1 for x in data["invalid"]["qcs"] if x < t)
        acc = corr / len(dataset)
        if acc > best_rho_acc:
            best_rho_acc = acc
            best_rho_thresh = t
            
    print(f"\nBest Rho Accuracy: {best_rho_acc:.1%} at Threshold: {best_rho_thresh:.2f}")

if __name__ == "__main__":
    analyze_distributions()
