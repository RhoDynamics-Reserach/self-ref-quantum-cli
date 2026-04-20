import json
import os
import sys
import numpy as np
from sklearn.metrics import roc_auc_score
from sentence_transformers import SentenceTransformer

# Adjust path to include src
sys.path.append(os.path.join(os.getcwd(), 'src'))
from rhodynamics import Lab

def calculate_metrics():
    # 1. Setup
    embedder = SentenceTransformer('all-MiniLM-L6-v2').encode
    lab = Lab(embedding_function=embedder, db_path=':memory:')
    
    data_path = 'examples/scientific_audit/SRD_100.json'
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found.")
        return

    with open(data_path, 'r') as f:
        srd = json.load(f)
    
    qcs = []
    truth = []

    print(f"Processing {len(srd)} samples...")
    for i, item in enumerate(srd):
        # Use unique names to prevent loading the same agent from disk for different topics
        agent_name = f"MetricAgent_{i}"
        agent = lab.get_or_create_agent(agent_name, knowledge=item['ground_truth'])
        _, m = lab.run_grounding_cycle(agent, item['query'], item['context'], evolve=False)
        qcs.append(m['confidence_score'])
        truth.append(item['is_valid'])
    
    # 2. Calculation
    corr = np.corrcoef(qcs, truth)[0,1]
    auc = roc_auc_score(truth, qcs)
    
    low_vals = [t for q,t in zip(qcs, truth) if q < 0.4]
    high_vals = [t for q,t in zip(qcs, truth) if q > 0.8]
    
    low_acc = sum(low_vals)/len(low_vals) if low_vals else 0
    high_acc = sum(high_vals)/len(high_vals) if high_vals else 0
    
    print("-" * 30)
    print(f"Correlation: {corr:.4f}")
    print(f"ROC AUC: {auc:.4f}")
    print(f"Low QCS accuracy: {low_acc:.4f}")
    print(f"High QCS accuracy: {high_acc:.4f}")
    print("-" * 30)
    
    # 3. Save results for the user
    results = [{'qcs': q, 'truth': t} for q,t in zip(qcs, truth)]
    with open('test_results.json', 'w') as f:
        json.dump(results, f, indent=4)
    print("Results saved to test_results.json")

if __name__ == "__main__":
    calculate_metrics()
