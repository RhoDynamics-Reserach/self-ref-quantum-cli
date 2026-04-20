import numpy as np

def amplitude_encoding(vector: np.ndarray):
    """
    Encodes a classical normalized vector into a quantum-like probability distribution.
    |psi> = sum(v_i |i>) -> returns |v_i|^2.
    """
    # 1. Normalize the vector (L2 norm)
    norm = np.linalg.norm(vector)
    if norm == 0:
        return np.zeros_like(vector)
    
    normalized_vec = vector / norm
    
    # 2. Get probabilities (Square of amplitudes)
    probabilities = np.abs(normalized_vec) ** 2
    
    return probabilities

def text_to_quantum_state(embedding: np.ndarray, num_qubits: int = 8):
    """
    Maps a high-dimensional embedding to a target qubit Hilbert space dimension (2^n).
    Uses a more stable pooling method to preserve semantic signals.
    """
    target_dim = 2 ** num_qubits
    
    if len(embedding) == 0:
        return np.zeros(target_dim)
        
    # Standardize embedding to have zero mean and unit variance before projection
    # This helps in dealing with different embedding models (Llama, OpenAI, etc.)
    emp_mean = np.mean(embedding)
    emp_std = np.std(embedding) + 1e-9
    norm_emb = (embedding - emp_mean) / emp_std
    
    # Mathematically Rigorous Gaussian Random Projection (JL-Lemma)
    # Plus a Quantum-inspired Sin-Cos Feature Mapping for Non-Linearity
    gen = np.random.default_rng(42)
    projection_matrix = gen.normal(0, 1.0 / np.sqrt(target_dim), (target_dim, len(norm_emb)))
    
    # 1. Linear Projection
    linear_projected = projection_matrix @ norm_emb
    
    # 2. Non-Linear Feature Mapping (Quantum-inspired Kernel)
    # This stretches the manifold to separate 'Sincere Lies' from Truths
    feature_mapped = np.sin(linear_projected) * np.cos(linear_projected * 0.5)
    
    # Quantum-inspired Amplitude-to-Probability mapping (|psi|^2)
    probabilities = np.abs(feature_mapped) ** 2
    
    # Final normalization into a valid probability distribution
    return probabilities / (np.sum(probabilities) + 1e-9)
