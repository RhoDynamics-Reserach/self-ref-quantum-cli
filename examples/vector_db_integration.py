import os
import sys
import requests
import numpy as np

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# Adjust path to import the local quantum_rag_layer
PACKAGE_PARENT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PACKAGE_PARENT not in sys.path:
    sys.path.append(PACKAGE_PARENT)

from quantum_rag_layer import QuantumMiddleware

# --- CONFIGURATION ---
OLLAMA_MODEL = "llama3"
OLLAMA_URL = "http://localhost:11434/api"

# --- 1. CUSTOM VECTOR STORE (Numpy-Based) ---
class SimpleQuantumStore:
    def __init__(self, embed_fn):
        self.embed_fn = embed_fn
        self.documents = []
        self.embeddings = []

    def add_documents(self, doc_list):
        print(f"[*] Ingesting {len(doc_list)} documents into the manifold...")
        for doc in doc_list:
            self.documents.append(doc)
            self.embeddings.append(self.embed_fn(doc))

    def retrieve(self, query, top_k=1):
        q_vec = self.embed_fn(query)
        # Cosine Similarity Calculation
        similarities = [np.dot(q_vec, d_vec) / (np.linalg.norm(q_vec) * np.linalg.norm(d_vec)) for d_vec in self.embeddings]
        top_idx = np.argmax(similarities)
        return self.documents[top_idx], similarities[top_idx]

# --- 2. LLM CONNECTOR ---
def call_ollama(prompt):
    try:
        r = requests.post(f"{OLLAMA_URL}/generate", json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}, timeout=30)
        return r.json()["response"].strip()
    except Exception as e:
        return f"Ollama Error: {e}"

def get_ollama_embedding(text):
    try:
        r = requests.post(f"{OLLAMA_URL}/embeddings", json={"model": OLLAMA_MODEL, "prompt": text}, timeout=10)
        return np.array(r.json()["embedding"])
    except:
        return np.random.rand(768)

def main():
    print("="*80)
    print(" >>> REAL-WORLD INTEGRATION: VECTOR DB + QUANTUM RAG LAYER <<<")
    print("="*80)

    # A. Initialize Local DB and Middleware
    db = SimpleQuantumStore(embed_fn=get_ollama_embedding)
    middleware = QuantumMiddleware(embedding_function=get_ollama_embedding)

    # B. Ingest Professional Context
    db.add_documents([
        "Policy-A: Remote workers must use a VPN at all times. Failure to do so logs a security vulnerability flag.",
        "Policy-B: PTO requests require 2 weeks notice minimum for approval by department leads.",
        "Policy-C: Our Quantum Synergy Engine uses Lindblad equations for non-linear stabilization."
    ])

    # C. Search & Quantum Filter Loop
    queries = [
        "What is the requirement for remote work?",
        "When will the Blue Octopus bite its prey?" 
    ]

    agent = middleware.create_agent("Corporate_Navigator", "You are a policy expert.")

    for q in queries:
        print(f"\n[QUERY] -> {q}")
        
        # 1. RETRIEVAL
        retrieved_doc, raw_similarity = db.retrieve(q)
        print(f"   [Retrieved Doc]: '{retrieved_doc[:50]}... ' (Sim: {raw_similarity:.2f})")

        # 2. QUANTUM FILTER
        final_prompt, metrics = middleware.process_query(agent, q, retrieved_doc)
        qcs = metrics["confidence_score"]
        
        print(f"   [Quantum Confidence Score]: {qcs:.2f} / 1.00")

        # 3. GENERATION
        print(f"   [Generating Response via Ollama]...")
        response = call_ollama(final_prompt)
        
        print(f"\n[FINAL AGENT RESPONSE]:\n{response}")
        print("-" * 50)

if __name__ == "__main__":
    main()
