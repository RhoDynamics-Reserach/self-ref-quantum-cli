from .middleware import QuantumMiddleware
from .rag_engine import QuantumRAGLayer
from .agent_model import BaseQuantumAgent
from .encoding import text_to_quantum_state
from .math_engine import calculate_zeta, calculate_chi_square, calculate_fitness
from .synergy import QuantumSynergyEngine
from . import adapters

__all__ = [
    "QuantumMiddleware",
    "QuantumRAGLayer",
    "BaseQuantumAgent",
    "QuantumSynergyEngine",
    "text_to_quantum_state",
    "calculate_zeta",
    "calculate_chi_square",
    "calculate_fitness",
    "adapters"
]

# Note: QuantumHardwareConnector is intentionally omitted from the root __init__ 
# to prevent mandatory Qiskit dependency at package import.
# Use: from rhodynamics.hardware_connector import QuantumHardwareConnector 
# for real QPU hardware execution.
