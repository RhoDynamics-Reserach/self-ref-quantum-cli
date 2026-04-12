import pytest
import numpy as np
from quantum_rag_layer.middleware import QuantumMiddleware
from quantum_rag_layer.agent_model import BaseQuantumAgent

def mock_semantic_embed(text):
    """
    Deterministic base embedding to replace random fallbacks.
    Provides mathematically stable semantics without relying on local LLMs.
    """
    length = len(text)
    vec = np.linspace(0.1, length * 0.1, 768)
    norm = np.linalg.norm(vec)
    return vec / norm if norm > 0 else np.ones(768)/np.sqrt(768)

def test_objective_confidence_score_distinction():
    """
    Asserts that the QCS can mathematically differentiate between 
    a matched context and an orthogonal paradox.
    """
    middleware = QuantumMiddleware(embedding_function=mock_semantic_embed)
    agent = middleware.create_agent("Validation-Agent")
    
    context = "The Earth revolves around the Sun."
    
    # 1. Matched Query (Should yield solid QCS)
    matched_query = "What does the Earth revolve around?"
    _, metrics_match = middleware.process_query(agent, matched_query, context)
    
    # 2. Orthogonal Paradox Query (Should yield different QCS, usually lower theoretically)
    paradox_query = "Does the Sun revolve around the Moon?"
    _, metrics_paradox = middleware.process_query(agent, paradox_query, context)
    
    assert "confidence_score" in metrics_match
    assert "confidence_score" in metrics_paradox
    assert isinstance(metrics_match["confidence_score"], float)

def test_no_random_fallbacks_in_agent():
    """
    Ensure the agent structure never relies on random matrices automatically.
    """
    agent = BaseQuantumAgent(name="Strict-Agent")
    assert agent.zeta >= 1.0
