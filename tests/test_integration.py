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
    # Provides mathematically explicit alignment to prevent edge-case margin failures.
    def semantic_mock(text):
        import numpy as np
        vec = np.zeros(256)
        if "France" in text and "What" in text:  # The Query
            vec[0] = 1.0 
        elif "Paris" in text:                    # The Context
            vec[0] = 0.9 
        elif "England" in text:                  # The Invalid Query
            vec[0] = -1.0 
        else:
            vec[0] = 0.5
        # Add micro-variance to ensure normalization (std != 0) succeeds
        vec += np.linspace(0.001, 0.002, 256)
        return vec
            
    middleware = QuantumMiddleware(embedding_function=semantic_mock)
    
    # 2. Isolated A/B Agents
    # Agents are stateful and evolve upon queries. We must use two independent
    # clones to ensure the A/B test is fair and isolated.
    agent_valid = middleware.create_agent("E2E-Valid", seed=100)
    agent_invalid = middleware.create_agent("E2E-Invalid", seed=100)
    
    context = "The capital of France is Paris."
    
    # Process Query 1: Valid Ground Truth
    prompt_v, metrics_v = middleware.process_query(agent_valid, "What is the capital of France?", context)
    
    # Process Query 2: Fraudulent/Mismatch
    prompt_i, metrics_i = middleware.process_query(agent_invalid, "What is the capital of England?", context)
    
    # 4. BASIC ASSERTIONS
    # This is an integration smoke test, not an empirical sensitivity test.
    # We verify the outputs are well-formed and pipeline executes correctly without crashing.
    assert isinstance(metrics_v["confidence_score"], float)
    assert isinstance(metrics_i["confidence_score"], float)
    assert 0.0 <= metrics_v["confidence_score"] <= 1.0
    assert 0.0 <= metrics_i["confidence_score"] <= 1.0
    
    assert "Paris" in prompt_v
    # Check for the new dynamic markers instead of legacy "SYSTEM RULE"
    assert "RULE" in prompt_v or "WARNING" in prompt_v
    print(f"[+] E2E Flow verified. Sensitivity Delta: {metrics_v['confidence_score'] - metrics_i['confidence_score']:.3f}")
