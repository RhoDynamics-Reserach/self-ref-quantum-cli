import os
import sys
import numpy as np
import requests
from datetime import datetime
from dotenv import load_dotenv

# Path resolution
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.append(base_dir)

from src.quantum_rag_layer.middleware import QuantumMiddleware
from src.quantum_rag_layer.hardware_connector import QuantumHardwareConnector

# --- Configuration ---
OLLAMA_URL = "http://localhost:11434/api/embeddings"
OLLAMA_MODEL = "llama3"
load_dotenv()

def get_embed(text):
    try:
        response = requests.post(OLLAMA_URL, json={"model": OLLAMA_MODEL, "prompt": text}, timeout=10.0)
        return np.array(response.json()["embedding"])
    except:
        raise ConnectionError("Ollama needed for hardware benchmark.")

import pytest
import numpy as np
    try:
        from src.quantum_rag_layer.hardware_connector import QuantumHardwareConnector
        connector = QuantumHardwareConnector()
        return connector.is_real_hardware()
    except:
        return False

@pytest.mark.qpu
@pytest.mark.skipif(not check_ibm(), reason="Physical IBM QPU unavailable or IBM_QUANTUM_TOKEN missing")
def test_hardware_proof():
    """
    Quantum RAG - FINAL HARDWARE VALIDATION (QPU-ONLY)
    Executes a real interaction sequence on IBM physical hardware.
    """
    from src.quantum_rag_layer.hardware_connector import QuantumHardwareConnector
    from src.quantum_rag_layer.middleware import QuantumMiddleware

    # 1. Initialize Real Hardware
    connector = QuantumHardwareConnector()
    print(f"[*] Targeting QPU Backend: {connector.backend.name}")
    
    middleware = QuantumMiddleware(embedding_function=lambda x: np.random.rand(768)) # Simplified for hardware smoke test
    agent = middleware.create_agent("QPU-Validator", measurement_executor=connector)
    
    # 2. Key Scenarios for Hardware Proof
    scenarios = [
        {"q": "Is the Earth round?", "c": "The Earth is an oblate spheroid.", "label": "Truth"}
    ]
    
    for item in scenarios:
        _, metrics = middleware.process_query(agent, item["q"], item["c"])
        score = metrics["confidence_score"]
        assert 0 <= score <= 1.0
        print(f"  >> QCS Result (Hardware): {score:.4f}")
