import numpy as np

class OllamaAdapter:
    """
    Adapter for seamless local LLM integration using Ollama.
    Provides embedding function for QuantumMiddleware and text generation.
    Requires `ollama` python package to be installed.
    """
    def __init__(self, model_name: str = "llama3", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        try:
            from ollama import Client
            self.client = Client(host=self.base_url)
        except ImportError:
            raise ImportError("The 'ollama' package is required. Run 'pip install ollama'")

    def embed(self, text: str) -> np.ndarray:
        """Generates embedding vector for the QuantumMiddleware."""
        response = self.client.embeddings(model=self.model_name, prompt=text)
        return np.array(response["embedding"])

    def generate_response(self, augmented_prompt: str) -> str:
        """Feeds the final Quantum-Augmented prompt to the model."""
        response = self.client.chat(model=self.model_name, messages=[
            {
                'role': 'user',
                'content': augmented_prompt
            }
        ])
        return response['message']['content']
