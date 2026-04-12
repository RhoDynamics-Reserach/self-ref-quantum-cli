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
    
    # Simple semantic pooling: Take N evenly spaced samples to represent the manifold
    # instead of averaging which can wash out signals in high-dim vectors.
    indices = np.linspace(0, len(embedding) - 1, target_dim, dtype=int)
    reduced_vec = norm_emb[indices]
    
    # Ensure all values are positive for amplitude encoding to avoid sign cancellations
    # if we were to treat them as probability amplitudes directly.
    # Actually, amplitude encoding uses absolute values, but let's shift to be safe.
    reduced_vec = np.abs(reduced_vec)
    
    return amplitude_encoding(reduced_vec)
