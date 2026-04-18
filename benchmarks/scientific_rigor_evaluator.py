import os
import sys
import json
import time
import numpy as np
from scipy import stats
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

# Adjust path to include src
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from rhodynamics import Lab

console = Console()

class IndustryBaseline:
    """Represents standard RAG (Cosine Similarity)."""
    def __init__(self):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def get_score(self, text1, text2):
        v1 = self.model.encode(text1)
        v2 = self.model.encode(text2)
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def run_rigor_benchmark():
    # 1. Setup
    with open('benchmarks/SRD_100.json', 'r') as f:
        dataset = json.load(f)
    
    baseline = IndustryBaseline()
    lab = Lab(embedding_function=baseline.model.encode, db_path=":memory:")
    
    results = {
        "baseline": [], # Binary: 1 if correct, 0 if wrong
        "rho": []
    }
    
    console.print(f"[bold blue]Starting Scientific Rigor Benchmark (N={len(dataset)})[/bold blue]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Evaluating samples...", total=len(dataset))
        
        for i, item in enumerate(dataset):
            query = item["query"]
            gt = item["ground_truth"]
            ctx = item["context"]
            label = item["is_valid"] # 1: Context is True, 0: Context is Hallucination
            
            # --- BASELINE (Cosine) ---
            cos_score = baseline.get_score(query, ctx)
            # Baseline "accepts" if cos_score > 0.5
            baseline_pred = 1 if cos_score >= 0.5 else 0
            results["baseline"].append(1 if baseline_pred == label else 0)
            
            # --- RHODYNAMICS (QCS) ---
            agent = lab.get_or_create_agent(f"RigorAgent_{i}", knowledge=gt)
            _, metrics = lab.run_grounding_cycle(agent, query, ctx, evolve=False)
            qcs = metrics["confidence_score"]
            # RhoDynamics "accepts" if QCS >= 0.5
            rho_pred = 1 if qcs >= 0.5 else 0
            results["rho"].append(1 if rho_pred == label else 0)
            
            progress.update(task, advance=1)

    # 2. Statistics calculation
    bl_acc = np.mean(results["baseline"])
    rho_acc = np.mean(results["rho"])
    
    # Statistical Significance (t-test for independent means)
    t_stat, p_val = stats.ttest_ind(results["baseline"], results["rho"])
    
    # Hallucination Rejection Rate (HRR) - Only for is_valid=0 samples
    invalid_indices = [idx for idx, item in enumerate(dataset) if item["is_valid"] == 0]
    bl_hrr = np.mean([results["baseline"][i] for i in invalid_indices])
    rho_hrr = np.mean([results["rho"][i] for i in invalid_indices])
    
    # 3. Visualization
    table = Table(title=f"Scientific Rigor Analysis (N={len(dataset)})")
    table.add_column("Metric", style="cyan")
    table.add_column("Classic RAG (Cosine)", justify="right")
    table.add_column("RhoDynamics (Q-RAG)", justify="right", style="bold green")
    
    table.add_row("Overall Accuracy", f"{bl_acc:.1%}", f"{rho_acc:.1%}")
    table.add_row("Hallucination Rejection Rate", f"{bl_hrr:.1%}", f"{rho_hrr:.1%}")
    table.add_row("Statistical Significance (P-Value)", "-", f"{p_val:.4f}")
    
    console.print(table)
    
    if p_val < 0.05:
        console.print("[bold green]Success: Result is Statistically Significant (p < 0.05)[/bold green]")
    else:
        console.print("[bold yellow]Wait: Result is not statistically significant yet.[/bold yellow]")

    # Save final report to docs
    os.makedirs('docs', exist_ok=True)
    report = {
        "n_samples": len(dataset),
        "baseline_accuracy": bl_acc,
        "rho_accuracy": rho_acc,
        "p_value": p_val,
        "baseline_hrr": bl_hrr,
        "rho_hrr": rho_hrr,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    with open('docs/scientific_rigor_report.json', 'w') as f:
        json.dump(report, f, indent=4)

if __name__ == "__main__":
    run_rigor_benchmark()
