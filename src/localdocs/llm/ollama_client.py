"""Ollama interaction client for local LLM processing"""
import requests
import logging
from typing import Optional
from localdocs.utils.config import settings

logger = logging.getLogger(__name__)

class OllamaClient:
    def __init__(self):
        # Use our global settings for the base URL
        self.base_url = settings.ollama_base_url
    
    def check_connection(self) -> bool:
        """Verify if the local Ollama service is reachable"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=3)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def generate_docs(self, code: str, model: Optional[str] = None) -> str:
        """Generate professional documentation using local LLM"""
        # Fall back to default model from settings if none specified
        selected_model = model or settings.default_model
        
        prompt = f"""
        Generate professional documentation for this code:
        
        {code}
        
        Include:
        - Function/class descriptions
        - Parameters and return types
        - Usage examples
        """
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": selected_model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60  # Give the model plenty of time to process on Termux
            )
            response.raise_for_stat_code() # Ensure we catch HTTP errors
            return response.json().get("response", "Error: No response text returned.")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to communicate with Ollama: {e}")
            return f"Error: Failed to connect to local LLM engine. Details: {e}"
