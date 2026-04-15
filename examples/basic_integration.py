import os
import sys

# Ensure the 'src' directory is in PYTHONPATH for local execution
# From 'examples/', '..' is root. Source is in 'src/'
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC_PATH = os.path.join(REPO_ROOT, "src")
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

import numpy as np
from rhodynamics.middleware import QuantumMiddleware

# 1. Define your embedding function (Mocking one for this example)
def dummy_embedding(text: str) -> np.ndarray:
    """In reality, use OpenAI, HuggingFace, or Ollama embeddings here"""
    return np.random.rand(768)

# 2. Initialize the Middleware
middleware = QuantumMiddleware(embedding_function=dummy_embedding)

# 3. Create your Chatbot's Quantum Persona
chatbot_agent = middleware.create_agent(
    name="SupportBot",
    base_knowledge_text="Customer support guidelines and technical documentation."
)

# 4. Integrate into your query pipeline
user_query = "How do I reset my password?"
retrieved_context = "To reset a password, navigate to settings > security."

print("Processing Query through Quantum RAG Layer...")

augmented_prompt, metrics = middleware.process_query(
    agent=chatbot_agent,
    query=user_query,
    context=retrieved_context
)

print(f"\n--- Quantum Confidence Score (QCS) ---")
print(f"[{metrics['confidence_score']:.2f}/1.00] - This measures semantic stability.")

print("\n--- Final Prompt to send to your LLM ---")
print(augmented_prompt)

# Next Step: Call your LLM, e.g. openai.ChatCompletion.create(messages=[{"role": "user", "content": augmented_prompt}])
