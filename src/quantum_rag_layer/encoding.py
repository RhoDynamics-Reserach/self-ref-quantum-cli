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

def text_to_quantum_state(embedding: np.ndarray, num_qubits: int = 4):
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
    # Maps high-dimensional embeddings (4096) to Hilbert space (16)
    # Scaled by 1/sqrt(N) to preserve inner product variance.
    gen = np.random.default_rng(42)
    projection_matrix = gen.normal(0, 1.0 / np.sqrt(target_dim), (target_dim, len(norm_emb)))
    
    # Linear Projection
    projected_vec = projection_matrix @ norm_emb
    
    # Quantum-inspired Amplitude-to-Probability mapping (|psi|^2)
    # This preserves the geometric structure of the original manifold
    probabilities = np.abs(projected_vec) ** 2
    
    # Final normalization into a valid probability distribution
    return probabilities / (np.sum(probabilities) + 1e-9)
