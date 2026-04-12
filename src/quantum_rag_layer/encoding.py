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
    
    # Chunk-wise pooling to preserve semantic manifold topology
    # Split the long embedding into target_dim (16) sectors
    chunk_size = len(embedding) // target_dim
    reduced_vec = []
    
    for i in range(target_dim):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < target_dim - 1 else len(embedding)
        chunk = norm_emb[start:end]
        # Using a non-linear activation (exp) to ensure positivity 
        # while emphasizing high-magnitude semantic signals
        reduced_vec.append(np.mean(np.exp(chunk)))
    
    reduced_vec = np.array(reduced_vec)
    
    # Re-normalize into a valid probability distribution (|psi|^2)
    return reduced_vec / (np.sum(reduced_vec) + 1e-9)
