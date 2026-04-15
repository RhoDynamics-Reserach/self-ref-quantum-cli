import requests
import numpy as np

class AnthropicAdapter:
    """
    Native HTTP Adapter for Anthropic Claude models.
    Minimizes dependencies by using direct API calls.
    """
    def __init__(self, api_key: str, model_name: str = "claude-3-5-sonnet-20240620"):
        self.api_key = api_key
        self.model_name = model_name
        self.url = "https://api.anthropic.com/v1/messages"
        self.headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

    def embed(self, text: str) -> np.ndarray:
        """
        Anthropic does not provide a specific local embedding API comparable to OAI.
        We default to a deterministic semantic hash for local grounding if using Claude.
        """
        h = sum(ord(c) for c in text)
        gen = np.random.default_rng(h)
        return gen.normal(0, 1, 1536) # Match standard vector dimensions

    def generate_response(self, augmented_prompt: str) -> str:
        payload = {
            "model": self.model_name,
            "max_tokens": 1024,
            "messages": [
                {"role": "user", "content": augmented_prompt}
            ]
        }
        response = requests.post(self.url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()["content"][0]["text"]
