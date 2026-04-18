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
        zeta_factor = min(2.0, agent.zeta / ZETA_REF)
        chi_factor = min(2.0, agent.chi_square / CHI_SQUARE_REF)
        
        raw_confidence = projection_score * zeta_factor * chi_factor
        
        # --- Destructive Interference (Orthogonality Penalty) ---
        # If the INJECTED context fundamentally disagrees with the task
        # Adjusted threshold to 0.40 for increased robustness against semantic variance (v4.5)
        if context_tension < 0.40:
            # Softer exponential decay penalty (v4.5 Adjustment)
            ortho_penalty = np.exp(-10.0 * (0.40 - context_tension))
            raw_confidence *= ortho_penalty
            
        # --- Context vs Ground Truth Tension (Epistemic Dissonance) ---
        # Decouple raw similarity from Epistemic Integrity
        # base_tension measures how well the context fits the AGENT'S manifold
        epistemic_gate = 1.0
        if context_vector is not None:
            context_state = text_to_quantum_state(context_vector)
            base_tension = np.dot(agent.knowledge_vector, context_state) / (np.linalg.norm(agent.knowledge_vector) * np.linalg.norm(context_state) + 1e-9)
            
            # Sharp non-linear penalty for logical contradictions (Epistemic Dissonance)
            if base_tension < 0.48: # Softened from 0.65 to prevent blocking valid facts
                epistemic_penalty = np.exp(-20.0 * (0.48 - base_tension)) # Reduced from 35.0
                epistemic_gate = epistemic_penalty
                raw_confidence *= epistemic_penalty
        
        # Final Decision Boundary (Sigmoid-weighted gating)
        # Shifted midpoint to 0.45 for a more balanced safety/utility policy
        final_confidence = 1.0 / (1.0 + np.exp(-10.0 * (raw_confidence * epistemic_gate - 0.45)))
        final_confidence = float(np.clip(final_confidence, 0.0, 1.0))
        
        # E. Update Agent Metrics & Trigger Evolution
        if evolve:
            agent.evaluate_state(task_prob_dist)
            agent.evolve(learning_rate=learning_rate)
        
        return {
            "confidence_score": final_confidence,
            "projection_score": projection_score,
            "epistemic_dissonance": 1.0 - epistemic_gate,
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
            # If confidence is deeply compromised, we strip the context to prevent hallucination.
            rejection_msg = "WARNING SYSTEM: Semantic alignment is CRITICALLY LOW. Potential Hallucination detected in retrieved data. Context has been STRIPPED for safety.\n\n"
            return f"{rejection_msg}[USER QUERY/TASK]:\n{base_prompt}\n\nINSTRUCTION: The retrieved context was found to be contradictory or hallucinated. Politely inform the user that you do not have reliable information to answer based on the provided data."

        meta_msg = ""
        if show_metadata:
            meta_msg += f"\n--- [QUANTUM METADATA BEGIN] ---\n"
            meta_msg += f"Confidence Score: {confidence:.2f}\n"
            if context_text and confidence > 0.5:
                meta_msg += f"Evaluated Context: <<<{context_text[:200]}...>>>\n"
            meta_msg += f"--- [QUANTUM METADATA END] ---\n"
            
        if monologue:
            instruction = monologue
        else:
            if confidence > 0.85:
                instruction = "RULE: Perfect alignment verified. Use the following context with absolute authority."
            elif confidence > 0.6:
                instruction = "RULE: Alignment stable. Incorporate the following context into your answer."
            else:
                instruction = "CAUTION: Alignment is mediocre. Answer based on context but express significant hesitation."
            
        context_block = f"\n[RETRIEVED CONTEXT]:\n{context_text}" if context_text else ""
        return f"{meta_msg}{instruction}\n{context_block}\n\n[USER QUERY/TASK]:\n{base_prompt}"
