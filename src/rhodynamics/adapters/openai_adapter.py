import numpy as np

class OpenAIAdapter:
    """
    Adapter for seamless Cloud LLM integration using OpenAI.
    Provides embedding function for QuantumMiddleware and text generation.
    Requires `openai` python package and an API key.
    """
    def __init__(self, api_key: str, model_name: str = "gpt-4o", embedding_model: str = "text-embedding-3-small"):
        self.model_name = model_name
        self.embedding_model = embedding_model
        try:
            import openai
            self.client = openai.OpenAI(api_key=api_key)
        except ImportError:
            raise ImportError("The 'openai' package is required. Run 'pip install openai'")

    def embed(self, text: str) -> np.ndarray:
        """Generates embedding vector for the QuantumMiddleware."""
        response = self.client.embeddings.create(
            input=text,
            model=self.embedding_model
        )
        return np.array(response.data[0].embedding)

    def generate_response(self, augmented_prompt: str) -> str:
        """Feeds the final Quantum-Augmented prompt to the model."""
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": augmented_prompt
                }
            ]
        )
        return response.choices[0].message.content
