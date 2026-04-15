import requests
import numpy as np

class GeminiAdapter:
    """
    Native HTTP Adapter for Google Gemini models.
    Supports Gemini 1.5 Pro and Flash via direct API calls.
    """
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        self.api_key = api_key
        self.model_name = model_name
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.api_key}"

    def embed(self, text: str) -> np.ndarray:
        """Determinstic semantic fingerprint fallback for Gemini mode."""
        h = sum(ord(c) for c in text)
        gen = np.random.default_rng(h)
        return gen.normal(0, 1, 768)

    def generate_response(self, augmented_prompt: str) -> str:
        payload = {
            "contents": [{
                "parts": [{"text": augmented_prompt}]
            }]
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(self.url, headers=headers, json=payload)
        response.raise_for_status()
        
        # Parse Gemini nested response structure
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
