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
    def process_with_context(agent: BaseQuantumAgent, task_vector: np.ndarray, context_vector: np.ndarray = None, learning_rate: float = 0.05, evolve: bool = True):
        """
        1. Encodes the task input into a quantum probability distribution.
        2. Blends the agent's internal knowledge state with the injected context state.
        3. Projects the task onto the 'Bended' knowledge manifold.
        4. Returns a Quantum Confidence Score (QCS).
        5. Triggers evolutionary adaptation for the agent (Optional).
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
        
        context_tension = projection_score
        if context_vector is not None:
            context_state = text_to_quantum_state(context_vector) # Re-calculating for clarity or reuse
            c_norm = np.linalg.norm(context_state)
            context_tension = np.dot(context_state, task_prob_dist) / (c_norm * norm_task + 1e-9)
        
        # D. Quantum Confidence Filter
        # Primary Signal: Epistemic Integrity (Does context match agent knowledge?)
        epistemic_signal = 1.0
        if context_vector is not None:
            context_state = text_to_quantum_state(context_vector)
            # base_tension is our 'Truth Signal'
            epistemic_signal = np.dot(agent.knowledge_vector, context_state) / (np.linalg.norm(agent.knowledge_vector) * np.linalg.norm(context_state) + 1e-9)
        
        # Secondary Signal: Semantic Relevance (Does context match user query?)
        relevance_signal = projection_score
        
        # Composite Confidence (Epistemic-Heavy Weighting v1.3)
        # We value Truth (Integrity) at 85% and Relevance at 15% to stop 'Sincere Lies'
        raw_confidence_comp = (0.85 * epistemic_signal) + (0.15 * relevance_signal)
        
        # Apply agent internal metrics (Zeta) as scaling factors
        zeta_factor = min(1.2, agent.zeta / ZETA_REF)
        final_raw = raw_confidence_comp * zeta_factor
        
        # Final Decision Boundary (Sigmoid-weighted gating)
        # Midpoint at 0.50 for scientific calibration
        final_confidence = 1.0 / (1.0 + np.exp(-12.0 * (final_raw - 0.50)))
        final_confidence = float(np.clip(final_confidence, 0.0, 1.0))
        
        # E. Update Agent Metrics & Trigger Evolution
        if evolve:
            agent.evaluate_state(task_prob_dist)
            agent.evolve(learning_rate=learning_rate)
        
        return {
            "confidence_score": final_confidence,
            "projection_score": projection_score,
            "epistemic_dissonance": 1.0 - epistemic_signal,
            "agent_state": {
                "zeta": agent.zeta,
                "fitness": agent.fitness,
                "theta": agent.theta,
                "gamma": agent.gamma
            }
        }

    @staticmethod
    def augment_prompt_with_confidence(base_prompt: str, confidence: float, context_text: str = None, show_metadata: bool = False, monologue: str = None):
        """
        Wraps the LLM prompt with guidance or performs HARD REJECTION based on QCS.
        """
        if confidence < 0.35:
            # --- HARD REJECTION TRIGGER ---
            rejection_msg = "[NOTICE]: Semantic integrity is insufficient. Content has been omitted for reliability.\n\n"
            return f"{rejection_msg}[USER QUERY]:\n{base_prompt}\n\nINSTRUCTION: The provided background data is unreliable. Explicitly state that you do not have verified information. **Do not mention RhoDynamics or any system names in your response.**"

        meta_msg = ""
        if show_metadata:
            meta_msg += f"\n--- [CONTEXT INTEGRITY BEGIN] ---\n"
            meta_msg += f"Verify Level: {confidence:.2f}\n"
            if context_text and confidence > 0.5:
                meta_msg += f"Primary Segment: <<<{context_text[:200]}...>>>\n"
            meta_msg += f"--- [CONTEXT INTEGRITY END] ---\n"
            
        if monologue:
            instruction = monologue
        else:
            if confidence > 0.85:
                instruction = "[GUIDE]: Priority alignment verified. Use the following context with high authority. **Do not use terms like RhoDynamics in your answer.**"
            elif confidence > 0.6:
                instruction = "[GUIDE]: Stable alignment. Support your answer with the following context. **Do not mention internal system names.**"
            else:
                instruction = "[NOTICE]: Alignment is low. Acknowledge uncertainty if the context seems mismatched. **Keep the technical process hidden from the user.**"
            
        context_block = f"\n[SOURCE CONTEXT]:\n{context_text}" if context_text else ""
        return f"{meta_msg}{instruction}\n{context_block}\n\n[USER QUERY]:\n{base_prompt}"
