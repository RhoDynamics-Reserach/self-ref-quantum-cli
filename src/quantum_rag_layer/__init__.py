from .middleware import QuantumMiddleware
from .rag_engine import QuantumRAGLayer
from .agent_model import BaseQuantumAgent
from .encoding import text_to_quantum_state
from .math_engine import calculate_zeta, calculate_chi_square, calculate_fitness

__all__ = [
    "QuantumMiddleware",
    "QuantumRAGLayer",
    "BaseQuantumAgent",
    "text_to_quantum_state",
    "calculate_zeta",
    "calculate_chi_square",
    "calculate_fitness"
]

# Note: QuantumHardwareConnector is intentionally omitted from the root __init__ 
# to prevent mandatory Qiskit dependency at package import.
# Use: from quantum_rag_layer.hardware_connector import QuantumHardwareConnector 
# for real QPU hardware execution.
