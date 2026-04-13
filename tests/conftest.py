import pytest
import requests
import os
from quantum_rag_layer.hardware_connector import QuantumHardwareConnector

# --- Service Availability Checks ---

def check_ollama():
    try:
        # Ping Ollama embeddings endpoint
        response = requests.post("http://localhost:11434/api/embeddings", json={"model": "llama3", "prompt": "test"}, timeout=2.0)
        return response.status_code == 200
    except:
        return False

def check_ibm():
    try:
        connector = QuantumHardwareConnector()
        return connector.is_real_hardware()
    except:
        return False

# --- Pytest Hooks/Markers ---

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "ollama: mark test as requiring a local Ollama service")
    config.addinivalue_line("markers", "qpu: mark test as requiring a real IBM QPU device")

# --- Fixtures ---

@pytest.fixture(scope="session")
def ollama_available():
    return check_ollama()

@pytest.fixture(scope="session")
def qpu_available():
    return check_ibm()

@pytest.fixture
def mock_embedding():
    """Provides a deterministic but non-identical embedding function for local testing."""
    def _embed(text):
        import numpy as np
        import hashlib
        # Create a 768-D vector seeded by text hash
        seed = int(hashlib.md5(text.encode()).hexdigest(), 16) % (2**32)
        rng = np.random.default_rng(seed)
        return rng.standard_normal(768)
    return _embed
