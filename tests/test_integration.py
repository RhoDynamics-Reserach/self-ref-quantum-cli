import pytest
import numpy as np
from rhodynamics import QuantumMiddleware, BaseQuantumAgent

def test_package_import_smoke():
    """
    Ensures the package and its core components can be imported without
    triggering heavy dependency errors or circular imports.
    """
    import rhodynamics
    from rhodynamics.middleware import QuantumMiddleware
    from rhodynamics.hardware_connector import QuantumHardwareConnector
    
    assert QuantumMiddleware is not None
    assert QuantumHardwareConnector is not None

def test_end_to_end_chatbot_flow(mock_embedding):
    # 1. Custom Semantic Mock
    # To prevent random noise from failing the test across different OS or NumPy versions,
    # we explicitly simulate semantic similarity.
    def semantic_mock(text):
        import numpy as np
        if "France" in text:
            return np.ones(256) * 0.8
        elif "England" in text:
            return np.ones(256) * -0.8
        else:
            return np.ones(256) * 0.5
            
    middleware = QuantumMiddleware(embedding_function=semantic_mock)
    agent = middleware.create_agent("E2E-Agent", seed=100)
    
    context = "The capital of France is Paris."
    
    # Process Query 1: Valid Ground Truth
    prompt_v, metrics_v = middleware.process_query(agent, "What is the capital of France?", context)
    
    # Process Query 2: Fraudulent/Mismatch
    prompt_i, metrics_i = middleware.process_query(agent, "What is the capital of England?", context)
    
    # 4. TIGHTENED ASSERTIONS
    # Paris should be treated as legitimate, while England should be flagged as orthogonal
    assert metrics_v["confidence_score"] > metrics_i["confidence_score"], \
        f"Sensitivity Error: Valid ({metrics_v['confidence_score']:.2f}) must exceed Invalid ({metrics_i['confidence_score']:.2f})"
    
    assert "Paris" in prompt_v
    # Check for the new dynamic markers instead of legacy "SYSTEM RULE"
    assert "RULE" in prompt_v or "WARNING" in prompt_v
    print(f"[+] E2E Flow verified. Sensitivity Delta: {metrics_v['confidence_score'] - metrics_i['confidence_score']:.3f}")
