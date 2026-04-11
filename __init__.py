from .agent_model import BaseQuantumAgent
from .rag_engine import QuantumRAGLayer
from .middleware import QuantumMiddleware
from .hardware_connector import QuantumHardwareConnector

# Export public API objects
__all__ = [
    "BaseQuantumAgent",
    "QuantumRAGLayer",
    "QuantumMiddleware",
    "QuantumHardwareConnector",
]

# Package metadata
__version__ = "1.0.0"
__author__ = "Quantum Synergy Group"
__description__ = "Hybrid Quantum-Classical Adaptive AI Layer"
