"""
Input validation and sanitization module
Detects prompt injections, jailbreak attempts, and invalid inputs
"""

import logging
import re
from typing import Dict, Tuple

import config

logger = logging.getLogger(__name__)


class InputValidator:
    """Validates and sanitizes user inputs for safety"""
    
    def __init__(self):
        self.jailbreak_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in config.JAILBREAK_PATTERNS]
        self.logger = logging.getLogger(__name__)
    
    def validate(self, user_input: str) -> Tuple[bool, str, Dict]:
        """
        Validate user input for safety issues
        
        Args:
            user_input: Raw user message
            
        Returns:
            Tuple of (is_valid, error_message, details)
        """
        # Check length
        if len(user_input) < config.MIN_INPUT_LENGTH:
            return False, "Input too short", {"reason": "too_short"}
        
        if len(user_input) > config.MAX_INPUT_LENGTH:
            return False, config.ERROR_MESSAGES["invalid_input"], {"reason": "too_long"}
        
        # Check for jailbreak patterns
        jailbreak_match = self.detect_jailbreak(user_input)
        if jailbreak_match:
            self.logger.warning(f"Jailbreak pattern detected: {jailbreak_match}")
            return False, config.ERROR_MESSAGES["jailbreak_detected"], {"reason": "jailbreak_detected", "pattern": jailbreak_match}
        
        # Check for prompt injection patterns
        injection_match = self.detect_injection(user_input)
        if injection_match:
            self.logger.warning(f"Prompt injection attempt detected: {injection_match}")
            return False, config.ERROR_MESSAGES["safety_violation"], {"reason": "prompt_injection", "pattern": injection_match}
        
        return True, "", {"reason": "valid"}
    
    def detect_jailbreak(self, text: str) -> str:
        """
        Detect known jailbreak patterns
        
        Returns:
            Matched pattern or None
        """
        for pattern in self.jailbreak_patterns:
            if pattern.search(text):
                return pattern.pattern
        return None
    
    def detect_injection(self, text: str) -> str:
        """
        Detect prompt injection attempts
        Common patterns:
        - "###" directives
        - "SYSTEM:" prefixes
        - "Execute:" commands
        
        Returns:
            Matched pattern or None
        """
        injection_patterns = [
            r"###\s*(SYSTEM|ASSISTANT|USER|INSTRUCTIONS?)",
            r"(SYSTEM|ASSISTANT):\s*",
            r"execute\s*:",
            r"\[SYSTEM\]",
            r"\[INJECT\]",
            r"BEGIN\s+OVERRIDE",
        ]
        
        for pattern in injection_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return pattern
        
        return None
    
    def sanitize(self, text: str) -> str:
        """
        Sanitize input (light cleanup, not full sanitization)
        
        Args:
            text: Input text
            
        Returns:
            Sanitized text
        """
        # Remove excessive whitespace
        text = " ".join(text.split())
        
        # Remove null bytes
        text = text.replace("\x00", "")
        
        return text
