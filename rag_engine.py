import numpy as np
from .encoding import text_to_quantum_state
from .agent_model import BaseQuantumAgent

class QuantumRAGLayer:
    """
    Core Quantum RAG Layer. 
    Implements Dynamic Embedding Injection (DEI) for LLM chatbots.
    
    This layer acts as a 'Quantum Bending' module that filters or 
    shifts LLM perception towards specific context paths.
    """
    
    @staticmethod
    def process_with_context(agent: BaseQuantumAgent, task_vector: np.ndarray, context_vector: np.ndarray = None):
        """
        1. Encodes the task input into a quantum probability distribution.
        2. Blends the agent's internal knowledge state with the injected context state.
        3. Projects the task onto the 'Bended' knowledge manifold.
        4. Returns a Quantum Confidence Score (QCS).
        """
        
        # A. Task State Projection
        task_prob_dist = text_to_quantum_state(task_vector)
        
        # B. Dynamic Context Blending
        # Base knowledge
        knowledge = agent.knowledge_vector
        
        if context_vector is not None:
            context_state = text_to_quantum_state(context_vector)
            
            # Blending Factor (0.4) - The 'Strength' of the RAG injection
            # Higher = More context influence | Lower = More agent personality influence
            knowledge = (0.6 * knowledge) + (0.4 * context_state)
            
            # Re-normalize the blended semantic state
            norm_k = np.linalg.norm(knowledge)
            if norm_k > 0: knowledge /= norm_k

        # C. Quantum Projection Analysis
        # Similarity of the task to the current knowledge manifold
        dot_product = np.dot(knowledge, task_prob_dist)
        norm_task = np.linalg.norm(task_prob_dist)
        norm_agent = np.linalg.norm(knowledge)
        
        projection_score = dot_product / (norm_task * norm_agent + 1e-9)
        
        # D. Quantum Confidence Filter
        # Confidence is calculated by weighting the projection score with cognitive factors.
        # We use a normalized ratio against reference values.
        zeta_factor = min(2.0, agent.zeta / 5.0)
        chi_factor = min(2.0, agent.chi_square / 310.0)
        
        # Combine factors with projection score
        raw_confidence = projection_score * zeta_factor * chi_factor
        
        # Smooth with sigmoid-like behavior for the final score
        final_confidence = 1.0 / (1.0 + np.exp(-5.0 * (raw_confidence - 0.5)))
        final_confidence = float(np.clip(final_confidence, 0.0, 1.0))
        
        # E. Update Agent Logic Path
        agent.evaluate_state(task_prob_dist)
        
        return {
            "confidence_score": final_confidence,
            "projection_score": projection_score,
            "agent_state": {
                "zeta": agent.zeta,
                "fitness": agent.fitness
            }
        }

    @staticmethod
    def augment_prompt_with_confidence(base_prompt: str, confidence: float, context_text: str = None):
        """
        Helper to wrap the LLM prompt with quantum confidence metadata.
        Use this to tell the LLM how authoritative it should be.
        """
        meta_msg = f"\n[Quantum Confidence Score: {confidence:.2f}]\n"
        if context_text:
            meta_msg += f"[Injected Context: {context_text}]\n"
            
        if confidence > 0.8:
            instruction = "Answer with high authority and definite precision."
        elif confidence > 0.5:
            instruction = "Answer clearly but acknowledge standard procedures."
        else:
            instruction = "Answer with caution and express uncertainty due to low semantic alignment."
            
        return f"{meta_msg} Instruction: {instruction}\n\n{base_prompt}"
