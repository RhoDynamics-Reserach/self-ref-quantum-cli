from typing import Callable, Any, Tuple, Optional
import numpy as np
from .agent_model import BaseQuantumAgent
from .rag_engine import QuantumRAGLayer
from .encoding import text_to_quantum_state

class QuantumMiddleware:
    """
    A high-level wrapper to easily integrate the Quantum RAG Engine 
    into any existing Chabot (OpenAI, Anthropic, Ollama, LangChain).
    """
    def __init__(self, embedding_function: Callable[[str], np.ndarray]):
        """
        Args:
            embedding_function: A function that takes a text string and returns a numpy/list embedding.
                                Example: lambda text: openai.Embedding.create(...)['data'][0]['embedding']
        """
        if not callable(embedding_function):
            raise ValueError("embedding_function must be a callable that returns an embedding vector.")
        self.embed_fn = embedding_function

    def create_agent(self, name: str, base_knowledge_text: Optional[str] = None, measurement_executor=None, seed: int = None) -> BaseQuantumAgent:
        """
        Initializes a Quantum Agent. 
        If base_knowledge_text is provided, it encodes it as the agent's fundamental semantic state.
        Now allows injecting a Real Hardware Executor and a deterministic Seed.
        """
        knowledge_vec = None
        if base_knowledge_text:
            raw_vec = self._safe_embed(base_knowledge_text)
            knowledge_vec = text_to_quantum_state(raw_vec)
            
        return BaseQuantumAgent(name=name, knowledge_vector=knowledge_vec, measurement_executor=measurement_executor, seed=seed)

    def process_query(self, agent: BaseQuantumAgent, query: str, context: str, show_metadata: bool = False) -> Tuple[str, dict]:
        """
        Takes a user's query and the retrieved context text (from your vector DB),
        processes them through the Quantum RAG pipeline, and returns the modified prompt.
        
        Args:
            show_metadata: If True, prints the QCS score directly into the LLM prompt.
                           Default is False (Silent Mode) for production use.
        """
        # 1. Embeddings
        query_vec = self._safe_embed(query)
        context_vec = self._safe_embed(context)
        
        # 2. Quantum Contextual State Processing
        q_result = QuantumRAGLayer.process_with_context(
            agent=agent,
            task_vector=query_vec,
            context_vector=context_vec
        )
        qcs = q_result["confidence_score"]
        
        # 3. Augment Prompt for the LLM
        base_prompt = f"Context: {context}\n\nQuestion: {query}"
        augmented_prompt = QuantumRAGLayer.augment_prompt_with_confidence(
            base_prompt=base_prompt,
            confidence=qcs,
            show_metadata=show_metadata
        )
        
        return augmented_prompt, q_result
        
    def _safe_embed(self, text: str) -> np.ndarray:
        """Safely calls the external embedding function and enforces numpy array format."""
        try:
            vec = self.embed_fn(text)
            if not isinstance(vec, np.ndarray):
                vec = np.array(vec)
            return vec
        except Exception as e:
            raise RuntimeError(f"Embedding function failed: {e}")
