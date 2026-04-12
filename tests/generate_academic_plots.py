import json
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def generate_academic_plot():
    # 1. Setup Data Paths
    base_dir = os.path.dirname(__file__)
    data_file = os.path.join(base_dir, "results", "qpu_final_benchmark.json")
    output_img = os.path.join(base_dir, "results", "final_evolution_plot.png")

    if not os.path.exists(data_file):
        print(f"Error: Data file not found at {data_file}")
        return

    # 2. Load Data
    with open(data_file, 'r') as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    # 3. Styling for Academic Journal (Nature/Science style)
    sns.set_theme(style="whitegrid", context="paper")
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman"],
        "axes.labelsize": 12,
        "axes.titlesize": 14,
        "legend.fontsize": 10,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "lines.linewidth": 2.5,
    })

    # 4. Create Dual-Axis Plot
    fig, ax1 = plt.subplots(figsize=(8, 5), dpi=300)

    # Primary Axis (Zeta - Stability)
    color1 = '#003366' # Deep Navy
    ax1.set_xlabel('Interaction Step (Sequential Dialogue)', weight='bold')
    ax1.set_ylabel(r'Cognitive Stability ($\zeta$)', color=color1, weight='bold')
    line1 = ax1.plot(df['step'], df['zeta'], marker='o', color=color1, label=r'Resilience ($\zeta$)', markersize=8)
    ax1.tick_params(axis='y', labelcolor=color1)
    
    # Optional: Add a shaded region for the 'baseline'
    ax1.axhline(y=df['zeta'].iloc[0], color='gray', linestyle='--', alpha=0.6, label='Baseline Initiation')

    # Secondary Axis (Theta - Phase Evolution)
    ax2 = ax1.twinx()  
    color2 = '#CC0000' # Deep Red
    ax2.set_ylabel(r'Agent Phase Angle ($\theta$)', color=color2, weight='bold')
    line2 = ax2.plot(df['step'], df['theta'], marker='s', color=color2, linestyle=':', label=r'Perspective ($\theta$)', markersize=8)
    ax2.tick_params(axis='y', labelcolor=color2)

    # 5. Title and Layout
    plt.title('Fig 2. Evolutionary Drift Analysis: Stability vs. Adaptation', pad=15, weight='bold')
    
    # Merge Legends
    lines = line1 + line2 + [ax1.get_lines()[0]]
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3, frameon=False)

    fig.tight_layout()

    # 6. Save
    plt.savefig(output_img, bbox_inches='tight')
    print(f"[*] Generated academic plot at: {output_img}")

if __name__ == "__main__":
    generate_academic_plot()
