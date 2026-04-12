import pytest
import numpy as np
from quantum_rag_layer import QuantumMiddleware, BaseQuantumAgent

def test_package_import_smoke():
    """
    Ensures the package and its core components can be imported without
    triggering heavy dependency errors or circular imports.
    """
    import quantum_rag_layer
    from quantum_rag_layer.middleware import QuantumMiddleware
    from quantum_rag_layer.hardware_connector import QuantumHardwareConnector
    
    assert QuantumMiddleware is not None
    assert QuantumHardwareConnector is not None

def test_end_to_end_chatbot_flow():
    """
    Simulates a full chatbot integration cycle:
    1. Middleware initialization with deterministic embedding.
    2. Agent creation.
    3. Context-aware query processing.
    4. Prompt augmentation verification.
    """
    # 1. Init
    def mock_embed(text):
        # Biased deterministic vector for high confidence
        vec = np.zeros(768)
        vec[0] = 1.0 # High alignment
        return vec
        
    middleware = QuantumMiddleware(embedding_function=mock_embed)
    
    # 2. Agent creation
    agent = middleware.create_agent("E2E-Agent", seed=100)
    assert isinstance(agent, BaseQuantumAgent)
    
    # 3. Process Query
    context = "The capital of France is Paris."
    query = "What is the capital of France?"
    
    prompt, metrics = middleware.process_query(agent, query, context)
    
    # 4. Assertions
    assert metrics["confidence_score"] > 0.5
    assert "Paris" in prompt
    assert "SYSTEM RULE" in prompt or "CRITICAL SYSTEM RULE" in prompt
    assert agent.zeta > 1.0 # Guaranteed by seed=100 for these params
    print(f"[+] E2E Flow verified. QCS: {metrics['confidence_score']:.2f}")
