import pytest
from rhodynamics import BaseQuantumAgent, QuantumSynergyEngine

def test_auto_sensory_monologue_generation():
    """
    Tests if the BaseQuantumAgent correctly translates its internal 
    mathematical state into the appropriate psychological string format.
    """
    agent = BaseQuantumAgent(name="SensoryBot")
    
    # Force High Coherence State
    agent.tau_m = 4.0
    agent.fitness = 0.8
    agent.zeta = 2.0
    
    monologue_high = agent.generate_cognitive_monologue()
    assert "High Coherence" in monologue_high
    assert "Memory Plasticity" in monologue_high
    
    # Force Sever Decoherence State
    agent.tau_m = 0.8
    agent.fitness = 0.2
    
    monologue_low = agent.generate_cognitive_monologue()
    assert "Severe Decoherence" in monologue_low
    assert "extreme skepticism" in monologue_low
    
    # Normal State
    agent.tau_m = 2.0
    agent.fitness = 0.5
    
    monologue_neutral = agent.generate_cognitive_monologue()
    assert "Learning State" in monologue_neutral
