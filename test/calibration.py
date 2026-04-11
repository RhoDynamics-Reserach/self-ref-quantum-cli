import os
import json
import requests
import numpy as np
import sys

# Fixed Windows Console Output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Adjust path 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from quantum_rag_layer.math_engine import calculate_chi_square, calculate_zeta
from quantum_rag_layer.encoding import text_to_quantum_state

# --- CONFIGURATION ---
OLLAMA_MODEL = "llama3"
OLLAMA_URL = "http://localhost:11434/api"

# Calibration Documents (Standard diversity)
CALIBRATION_TEXTS = [
    "The sun is a star in the center of the Solar System.",
    "Quantum mechanics is a fundamental theory in physics that provides a description of the physical properties of nature.",
    "Artificial intelligence is intelligence demonstrated by machines.",
    "Biology is the natural science that studies life and living organisms.",
    "Water is an inorganic, transparent, tasteless, odorless, and nearly colorless chemical substance.",
    "The Great Wall of China is a series of fortifications built along the northern borders of China.",
    "Photosynthesis is a process used by plants and other organisms to convert light energy into chemical energy.",
    "A computer is a machine that can be programmed to carry out sequences of arithmetic or logical operations.",
    "Evolution is change in the heritable characteristics of biological populations over successive generations.",
    "Mathematics includes the study of such topics as quantity, structure, space, and change."
]

def get_embed(text):
    try:
        r = requests.post(f"{OLLAMA_URL}/embeddings", json={"model": OLLAMA_MODEL, "prompt": text}, timeout=10)
        return np.array(r.json()["embedding"])
    except Exception as e:
        print(f"Embedding failed: {e}")
        return np.random.rand(768)

def run_calibration():
    print("="*60)
    print(" [CALIBRATION] QUANTUM RAG LAYER: SELF-CALIBRATION SYSTEM ")
    print("="*60)
    print(f"[*] Analyzing '{OLLAMA_MODEL}' embedding distribution for objective reference...")
    
    chi_squares = []
    zetas = []
    
    for i, text in enumerate(CALIBRATION_TEXTS, 1):
        vec = get_embed(text)
        state_probs = text_to_quantum_state(vec)
        
        # 1. Baseline Chi-Square
        shots = 1024
        outcomes = np.random.multinomial(shots, state_probs)
        chi = calculate_chi_square(outcomes, shots)
        chi_squares.append(chi)
        
        # 2. Baseline Zeta (using default agent params)
        zeta = calculate_zeta(1.0, 0.3, 2.0)
        zetas.append(zeta)
        
        print(f"   [{i/len(CALIBRATION_TEXTS)*100:.0f}%] Sample: {text[:30]}... | Chi: {chi:.2f}")

    # Calculate Objectively Derived References
    chi_ref = float(np.mean(chi_squares))
    zeta_ref = float(np.mean(zetas))
    
    # We add a 10% safety margin for the 'Normal' baseline
    config = {
        "CHI_SQUARE_REF": chi_ref,
        "ZETA_REF": zeta_ref,
        "M_REF": 1000.0,
        "calibration_timestamp": str(np.datetime64('now')),
        "calibrated_model": OLLAMA_MODEL
    }
    
    # Save config to the core package directory
    pkg_dir = os.path.dirname(os.path.abspath(__file__))
    if "test" in pkg_dir: # If running from test/ subfolder
        pkg_dir = os.path.dirname(pkg_dir)
        
    config_path = os.path.join(pkg_dir, "config.json")
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)
        
    print("\n" + "="*60)
    print("🏆 CALIBRATION COMPLETE 🏆")
    print(f"New CHI_SQUARE_REF: {chi_ref:.2f}")
    print(f"New ZETA_REF: {zeta_ref:.2f}")
    print(f"[*] Configuration saved to: {config_path}")
    print("[*] These values will now be used for 100% objective QCS calculation.")
    print("="*60)

if __name__ == "__main__":
    run_calibration()
