"""
Ollama Client for Local AI Processing
======================================
Communicates with local Ollama instance for documentation generation
"""

import subprocess
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class OllamaClient:
    """Client for interacting with local Ollama LLM."""
    
    def __init__(self, model: str = "llama3", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
    
    def generate_docs(self, elements: List[Dict[str, Any]]) -> str:
        """
        Generate documentation for code elements using Ollama.
        
        Args:
            elements: List of parsed code elements
            
        Returns:
            Generated documentation string
        """
        if not elements:
            return "No code elements found."
        
        # Build prompt for Ollama
        prompt = self._build_documentation_prompt(elements)
        
        try:
            # Call Ollama via CLI
            result = subprocess.run(
                ["ollama", "run", self.model, prompt],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                documentation = result.stdout.strip()
                logger.info(f"Generated documentation for {len(elements)} elements")
                return documentation
            else:
                logger.error(f"Ollama error: {result.stderr}")
                return "Error generating documentation. Please check Ollama is running."
                
        except subprocess.TimeoutExpired:
            logger.error("Ollama request timed out")
            return "Documentation generation timed out. Please try again."
        except Exception as e:
            logger.error(f"Error calling Ollama: {str(e)}")
            return f"Error: {str(e)}"
    
    def _build_documentation_prompt(self, elements: List[Dict[str, Any]]) -> str:
        """Build a prompt for generating documentation."""
        prompt = "Generate professional documentation for the following code elements:

"
        
        for element in elements:
            prompt += f"- {element['type'].upper()}: {element['name']}
"
            prompt += f"  Description: {element['description']}

"
        
        prompt += "
Please provide clear, comprehensive documentation including:
"
        prompt += "1. Overview of what this code does
"
        prompt += "2. Function/class descriptions
"
        prompt += "3. Parameters and return values
"
        prompt += "4. Usage examples if applicable
"
        
        return prompt
