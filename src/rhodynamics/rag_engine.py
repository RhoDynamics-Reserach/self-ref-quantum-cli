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
        
        # Born Rule: Probability is the square of the Amplitude (Dot Product)
        projection_score = (dot_product / (norm_task * norm_agent + 1e-9)) ** 2
        
        context_tension = projection_score
        if context_vector is not None:
            context_state = text_to_quantum_state(context_vector) # Re-calculating for clarity or reuse
            c_norm = np.linalg.norm(context_state)
            context_tension = (np.dot(context_state, task_prob_dist) / (c_norm * norm_task + 1e-9)) ** 2
        
        # D. Quantum Confidence Filter
        # Primary Signal: Epistemic Integrity (Context vs Knowledge)
        epistemic_signal = 1.0
        if context_vector is not None:
            context_state = text_to_quantum_state(context_vector)
            # Born Rule again
            epistemic_signal = (np.dot(agent.knowledge_vector, context_state) / (np.linalg.norm(agent.knowledge_vector) * np.linalg.norm(context_state) + 1e-9)) ** 2
        
        # Secondary Signal: Semantic Relevance (Context vs Query)
        # If context is provided, measure pure direct relevance (task vs context) without agent memory dilution
        relevance_signal = context_tension if context_vector is not None else projection_score
        
        # --- NON-LINEAR DISSONANCE ORACLE (v2.5) ---
        # Integrated with Sin-Cos Feature Mapping for higher contrast
        t_ref = 0.50 
        epistemic_gate = 1.0
        if epistemic_signal < t_ref:
            # Aggressive Cubic Penalty for Hallucinations
            epistemic_gate = np.exp(-12.0 * ((t_ref - epistemic_signal)**3))
        
        # --- DYNAMIC MANIFOLD ANCHORING (v3.0) ---
        # Integrate Zeta (stability) into the decision boundary
        # A more stable agent (higher zeta) is more 'opinionated' and strict
        strictness_factor = min(1.5, agent.zeta / ZETA_REF)
        
        # Composite weighting v3.0 (Zeta-Modulated)
        # Shifted to a 40/60 split for base agents to prevent epistemic signal from 
        # completely drowning out the semantic task tension.
        e_weight = 0.40 * strictness_factor
        r_weight = 1.0 - e_weight
        
        raw_confidence_comp = (e_weight * epistemic_signal * epistemic_gate) + (r_weight * relevance_signal)
        
        # Final Decision Boundary (Zeta-Anchored Sigmoid)
        # Shifted midpoint to 0.82 to bracket high-dimensional sentence embedding norms
        # Steepness set to 25.0 to force sharp separation between Truth (>0.80) and Hallucination (<0.35)
        midpoint = 0.82
        final_confidence = 1.0 / (1.0 + np.exp(-25.0 * (raw_confidence_comp - midpoint)))
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
