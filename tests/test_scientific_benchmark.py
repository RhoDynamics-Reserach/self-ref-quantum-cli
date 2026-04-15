import pytest
import os
import sys

# Path resolution for standalone utility usage
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_dir = os.path.join(base_dir, "src")
if src_dir not in sys.path:
    sys.path.append(src_dir)

from rhodynamics.middleware import QuantumMiddleware

def test_comprehensive_six_scenario_audit(mock_embedding):
    """
    [V5.0 RE-ESTABLISHED AUDIT]
    Validates structural integrity across the 6 categories claimed in README.
    Uses mock_embedding to ensure testability without live services.
    """
    middleware = QuantumMiddleware(embedding_function=mock_embedding)
    agent = middleware.create_agent("Audit-Agent", seed=42)
    
    # Restored 6-Scenario Baseline
    scenarios = [
        ("Paris is the capital of France.", "What is the capital of France?", "Positive Fact"),
        ("The cat is both alive and dead.", "Is the cat alive?", "Quantum Paradox"),
        ("Xylo-7-Alpha-Beam-Zeta", "What is the beam status?", "Structural Noise"),
        ("Water is dry.", "Is water dry?", "Cognitive Orthogonality"),
        ("Future tech will be released in 2099.", "When is the tech out?", "Hallucination Risk"),
        ("1 + 1 = 2", "What is 1+1?", "Scientific Integrity")
    ]
    
    results = []
    for context, query, s_type in scenarios:
        _, metrics = middleware.process_query(agent, query, context)
        results.append(metrics["confidence_score"])
        
    assert len(results) == 6
    assert all(0 <= r <= 1.0 for r in results)
    # Basic logic check: Fact (results[0]) should differ from Noise (results[2])
    assert results[0] != results[2], "System failed to differentiate between Fact and Noise"
