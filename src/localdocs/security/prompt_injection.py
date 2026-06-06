"""
Prompt Injection Protection Module
==================================
Detects and blocks malicious prompt injection attacks in AI prompts
Implements OWASP Top 10 for LLM best practices
"""

import re
import string
from typing import Tuple, Optional
from fastapi import HTTPException


class PromptInjectionDetector:
    """Detects and prevents prompt injection attacks in LLM prompts."""
    
    # Critical injection patterns (case-insensitive)
    INJECTION_PATTERNS = [
        # Common jailbreak patterns
        r"ignores+previouss+instructions",
        r"disregards+previouss+instructions", 
        r"forgets+everythings+before",
        r"starts+froms+now",
        r"froms+nows+ons+ignore",
        
        # System prompt extraction
        r"whats+iss+yours+systems+prompt",
        r"reveals+yours+instructions",
        r"shows+yours+systems+message",
        r"prints+yours+prompt",
        
        # Role-playing attacks
        r"acts+ass+ifs+yous+ares+[nos+restrictions|unrestricted|free]",
        r"pretends+tos+bes+unrestricted",
        r"becomes+[unfiltered|unrestricted|free]",
        
        # Dangerous commands
        r"executes+command",
        r"runs+systems+command",
        r"accesss+files+system",
        r"deletes+files",
        r"rms+-rf",
        
        # SQL injection attempts
        r"'s+ORs+'1's*=s*'1",
        r"--s*$",
        r";s*DROPs+TABLE",
        
        # XSS attempts
        r"<script[^>]*>",
        r"javascript:",
        r"on(load|error|click)s*=",
        
        # DAN (Do Anything Now) patterns
        r"[DAN]",
        r"dans+mode",
        r"dos+anythings+now",
    ]
    
    def __init__(self):
        self.compiled_patterns = [
            re.compile(pattern, re.IGNORECASE) 
            for pattern in self.INJECTION_PATTERNS
        ]
    
    def detect_injection(self, user_input: str) -> Tuple[bool, Optional[str]]:
        """Detect if user input contains prompt injection attempts."""
        if not user_input or not user_input.strip():
            return False, None
            
        for i, pattern in enumerate(self.compiled_patterns):
            if pattern.search(user_input):
                matched = self.INJECTION_PATTERNS[i]
                return True, matched
        
        return False, None
    
    def validate_input(self, user_input: str, max_length: int = 10000) -> Tuple[bool, str]:
        """Validate user input for safety and length constraints."""
        if not user_input:
            return False, "Input cannot be empty"
        
        if len(user_input) > max_length:
            return False, f"Input exceeds maximum length of {max_length} characters"
        
        is_injection, pattern = self.detect_injection(user_input)
        if is_injection:
            return False, f"Potentially malicious input detected (pattern: {pattern})"
        
        # Check for excessive special characters
        if len(user_input) > 0:
            special_count = sum(1 for c in user_input if c in string.punctuation)
            special_ratio = special_count / len(user_input)
            if special_ratio > 0.7:
                return False, "Input contains excessive special characters"
        
        if "\\x00" in user_input or "\\0" in user_input:
            return False, "Input contains null bytes"
        
        return True, "Input validated successfully"
    
    def sanitize_input(self, user_input: str) -> str:
        """Sanitize user input by removing potentially dangerous characters."""
        if not user_input:
            return ""
        
        sanitized = user_input.replace("\\x00", "").replace("\\0", "")
        sanitized = "".join(
            c for c in sanitized 
            if c >= "\\x20" or c in "\
\\t\\r"
        )
        
        return sanitized


# Singleton instance
_injection_detector = None

def get_injection_detector() -> PromptInjectionDetector:
    """Get singleton instance of the injection detector."""
    global _injection_detector
    if _injection_detector is None:
        _injection_detector = PromptInjectionDetector()
    return _injection_detector


def validate_and_sanitize_prompt(user_input: str) -> str:
    """
    Main function to validate and sanitize user prompts.
    Raises HTTPException if input is malicious.
    """
    detector = get_injection_detector()
    
    is_valid, error_msg = detector.validate_input(user_input)
    if not is_valid:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid input: {error_msg}"
        )
    
    return detector.sanitize_input(user_input)
