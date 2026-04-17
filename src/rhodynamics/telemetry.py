import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from .agent_model import BaseQuantumAgent
import numpy as np

class AgentTelemetry:
    """
    Scientific Telemetry module for generating academic-grade visualizations.
    """
    
    @staticmethod
    def _setup_academic_style():
        sns.set_theme(style="whitegrid", context="paper")
        plt.rcParams.update({
            "font.family": "serif",
            "font.serif": ["Times New Roman", "DejaVu Serif"],
            "axes.labelsize": 12,
            "axes.titlesize": 14,
            "legend.fontsize": 10,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "lines.linewidth": 2.5,
        })

    @staticmethod
    def plot_evolution(agent: BaseQuantumAgent, output_path: str = "evolution_plot.png"):
        """
        Generates a dual-axis plot showing Zeta (Stability) vs Delta M (Divergence)
        over the agent's interaction history.
        """
        if not agent.history:
            print("No history available to plot.")
            return None

        AgentTelemetry._setup_academic_style()
        
        df = pd.DataFrame(agent.history)
        df['step'] = range(1, len(df) + 1)
        
        fig, ax1 = plt.subplots(figsize=(8, 5), dpi=300)
        
        # Primary Axis (Zeta - Stability)
        color1 = '#003366' # Deep Navy
        ax1.set_xlabel('Interaction Step', weight='bold')
        ax1.set_ylabel(r'Cognitive Stability ($\zeta$)', color=color1, weight='bold')
        line1 = ax1.plot(df['step'], df['zeta'], marker='o', color=color1, label=r'Resilience ($\zeta$)')
        ax1.tick_params(axis='y', labelcolor=color1)
        
        if 'delta_M' in df.columns:
            # Secondary Axis (Divergence)
            ax2 = ax1.twinx()  
            color2 = '#CC0000' # Deep Red
            ax2.set_ylabel(r'Manifold Divergence ($\Delta M$)', color=color2, weight='bold')
            line2 = ax2.plot(df['step'], df['delta_M'], marker='s', color=color2, linestyle=':', label=r'Drift ($\Delta M$)')
            ax2.tick_params(axis='y', labelcolor=color2)
            lines = line1 + line2
        else:
            lines = line1
            
        plt.title(f'Evolutionary Drift Analysis: {agent.name}', pad=15, weight='bold')
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, frameon=False)
        
        fig.tight_layout()
        plt.savefig(output_path, bbox_inches='tight')
        plt.close()
        return output_path
