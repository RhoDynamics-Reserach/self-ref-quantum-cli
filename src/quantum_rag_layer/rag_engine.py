import numpy as np
from .math_engine import calculate_zeta, calculate_fitness, calculate_chi_square, ZETA_REF, CHI_SQUARE_REF
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
    def process_with_context(agent: BaseQuantumAgent, task_vector: np.ndarray, context_vector: np.ndarray = None, learning_rate: float = 0.05):
        """
        1. Encodes the task input into a quantum probability distribution.
        2. Blends the agent's internal knowledge state with the injected context state.
        3. Projects the task onto the 'Bended' knowledge manifold.
        4. Returns a Quantum Confidence Score (QCS).
        5. Triggers evolutionary adaptation for the agent.
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
            agent._last_context_state = context_state
            
            # Re-normalize the blended semantic state
            norm_k = np.linalg.norm(knowledge)
            if norm_k > 0: knowledge /= norm_k

        # C. Quantum Projection Analysis
        # Similarity of the task to the current knowledge manifold
        dot_product = np.dot(knowledge, task_prob_dist)
        norm_task = np.linalg.norm(task_prob_dist)
        norm_agent = np.linalg.norm(knowledge)
        
        projection_score = dot_product / (norm_task * norm_agent + 1e-9)
        
        # Calculate isolated context-to-task tension (Classical-Quantum Orthogonality)
        context_tension = projection_score
        if getattr(agent, "_last_context_state", None) is not None:
            # We must evaluate if the INJECTED context is irrelevant, not just the whole agent
            c_norm = np.linalg.norm(agent._last_context_state)
            if c_norm > 0:
                context_tension = np.dot(agent._last_context_state, task_prob_dist) / (c_norm * norm_task + 1e-9)
        
        # D. Quantum Confidence Filter
        zeta_factor = min(2.0, agent.zeta / ZETA_REF)
        chi_factor = min(2.0, agent.chi_square / CHI_SQUARE_REF)
        
        raw_confidence = projection_score * zeta_factor * chi_factor
        
        # --- Destructive Interference (Orthogonality Penalty) ---
        # If the INJECTED context fundamentally disagrees with the task
        if context_tension < 0.70:
            # Steep exponential decay penalty
            ortho_penalty = np.exp(-20.0 * (0.70 - context_tension))
            raw_confidence *= ortho_penalty
        
        # Smooth with sigmoid-like behavior for the final score
        final_confidence = 1.0 / (1.0 + np.exp(-5.0 * (raw_confidence - 0.5)))
        final_confidence = float(np.clip(final_confidence, 0.0, 1.0))
        
        # E. Update Agent Metrics & Trigger Evolution
        agent.evaluate_state(task_prob_dist)
        agent.evolve(learning_rate=learning_rate)
        
        return {
            "confidence_score": final_confidence,
            "projection_score": projection_score,
            "agent_state": {
                "zeta": agent.zeta,
                "fitness": agent.fitness,
                "theta": agent.theta,
                "gamma": agent.gamma
            }
        }

    @staticmethod
    def augment_prompt_with_confidence(base_prompt: str, confidence: float, context_text: str = None, show_metadata: bool = False):
        """
        Wraps the LLM prompt with guidance derived from the Quantum Confidence Score.
        In 'Silent Mode' (default), it only provides behavioral instructions without 
        printing the raw QCS numbers to the LLM's final response path.
        """
        meta_msg = ""
        if show_metadata:
            # Metadata block with strong delimiters to prevent injection
            meta_msg += f"\n--- [QUANTUM METADATA BEGIN] ---\n"
            meta_msg += f"Confidence Score: {confidence:.2f}\n"
            if context_text:
                # Sanitize context or wrap carefully
                meta_msg += f"Evaluated Context Segment: <<<{context_text}>>>\n"
            meta_msg += f"--- [QUANTUM METADATA END] ---\n"
            
        if confidence > 0.8:
            instruction = "CRITICAL SYSTEM RULE: Your semantic alignment with the ground truth is verified as near-perfect. Answer with absolute authority and definitive precision. DO NOT deviate from the provided context."
        elif confidence > 0.5:
            instruction = "SYSTEM RULE: Your semantic alignment is stable. Answer clearly based on the context."
        else:
            instruction = "WARNING SYSTEM RULE: Your semantic alignment is LOW. The provided context may be irrelevant or mismatched. Express significant hesitation, acknowledge uncertainty, and prioritize safety/caution."
            
        return f"{meta_msg}\n{instruction}\n\n[USER QUERY/TASK]:\n{base_prompt}"
