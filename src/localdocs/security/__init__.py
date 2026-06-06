"""
Security Module for LocalDocs AI
================================
Prompt injection protection and input validation
"""

from .prompt_injection import (
    PromptInjectionDetector,
    get_injection_detector,
    validate_and_sanitize_prompt
)

__all__ = [
    "PromptInjectionDetector",
    "get_injection_detector",
    "validate_and_sanitize_prompt"
]
