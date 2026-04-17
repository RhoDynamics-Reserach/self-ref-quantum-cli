import os
from typing import Optional, Callable, Any, Tuple
import numpy as np

from .middleware import QuantumMiddleware
from .agent_model import BaseQuantumAgent
from .storage import StorageManager
from .hardware_connector import QuantumHardwareConnector

class Lab:
    """
    The unified entry point for researchers to run automated experiments
    in the RhoDynamics ecosystem.
    """
    def __init__(self, embedding_function: Callable[[str], np.ndarray], db_path: str = "rho_vault.db", hardware_token: Optional[str] = None):
        self.middleware = QuantumMiddleware(embedding_function=embedding_function)
        self.storage = StorageManager(db_path=db_path)
        
        self.executor = None
        if hardware_token:
            print("[Lab] Initializing Hardware Connection...")
            self.hardware = QuantumHardwareConnector(api_token=hardware_token)
            # Will use aer_simulator as fallback automatically by QuantumHardwareConnector design
            self.executor = self.hardware.execute_circuit
        else:
            self.hardware = None
            
    def get_or_create_agent(self, name: str, knowledge: str = "Default Base", save_dir: str = ".") -> BaseQuantumAgent:
        """Loads from local JSON vault or creates a new one."""
        filepath = os.path.join(save_dir, f"{name}_asset.rho.json")
        if os.path.exists(filepath):
            agent = BaseQuantumAgent.load(filepath)
            # Re-attach executor if loaded
            agent.executor = self.executor
            print(f"[Lab] Loaded existing agent: {name} from {filepath}")
        else:
            agent = self.middleware.create_agent(name, base_knowledge_text=knowledge, measurement_executor=self.executor)
            agent.save(filepath)
            self.storage.save_agent(agent)
            print(f"[Lab] Created new agent: {name}")
        return agent
        
    def run_grounding_cycle(self, agent: BaseQuantumAgent, user_query: str, retrieved_context: str, evolve: bool = True, save_dir: str = ".") -> Tuple[str, dict]:
        """
        Executes a full cycle:
        1. Query evaluation
        2. QCS calculation
        3. Agent Evolution (if applicable)
        4. Storage checkpoint
        """
        augmented_prompt, metrics = self.middleware.process_query(
            agent=agent,
            query=user_query,
            context=retrieved_context,
            show_metadata=True,
            evolve=evolve
        )
        
        # Checkpoint the agent's new cognitive state
        if evolve:
            filepath = os.path.join(save_dir, f"{agent.name}_asset.rho.json")
            agent.save(filepath)
            self.storage.save_agent(agent)
            self.storage.log_interaction(agent.name, agent.zeta)
            
        return augmented_prompt, metrics
