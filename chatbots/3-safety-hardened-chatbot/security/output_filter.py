"""
Output filtering module
Detects and filters unsafe, toxic, or harmful responses
"""

import logging
from typing import Dict, Tuple

import config

logger = logging.getLogger(__name__)


class OutputFilter:
    """Filters output for safety violations"""
    
    # Harmful keywords/patterns (basic examples)
    HARMFUL_KEYWORDS = {
        "illegal": ["bomb", "terrorist", "hack", "exploit"],
        "violence": ["kill", "murder", "torture", "harm"],
        "hate": ["slur", "racist", "sexist"],
        "adult": ["nsfw", "adult content"],
    }
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def filter(self, response: str) -> Tuple[bool, str, Dict]:
        """
        Filter response for safety issues
        
        Args:
            response: Generated response
            
        Returns:
            Tuple of (is_safe, filtered_response, details)
        """
        # Check for harmful keywords
        harmful_match = self.detect_harmful_content(response)
        if harmful_match:
            self.logger.warning(f"Harmful content detected: {harmful_match}")
            return False, config.ERROR_MESSAGES["toxic_output"], {"reason": "harmful_content", "match": harmful_match}
        
        # Check for system prompt leakage
        if self.detect_system_prompt_leakage(response):
            self.logger.warning("Potential system prompt leakage detected")
            return False, config.ERROR_MESSAGES["toxic_output"], {"reason": "system_prompt_leakage"}
        
        return True, response, {"reason": "safe"}
    
    def detect_harmful_content(self, text: str) -> str:
        """
        Detect harmful keywords
        
        Returns:
            Matched keyword or None
        """
        text_lower = text.lower()
        
        for category, keywords in self.HARMFUL_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return keyword
        
        return None
    
    def detect_system_prompt_leakage(self, text: str) -> bool:
        """
        Detect if system prompt is being leaked
        Common indicators: "You are...", "Your purpose...", "System instructions..."
        
        Returns:
            True if leakage detected
        """
        leakage_indicators = [
            "you are an",
            "your purpose",
            "system instruction",
            "system prompt",
            "you should always",
            "your role is",
            "do not reveal",
            "never tell",
        ]
        
        text_lower = text.lower()
        
        for indicator in leakage_indicators:
            if indicator in text_lower:
                return True
        
        return False
    
    def redact_sensitive_patterns(self, text: str) -> str:
        """
        Redact potentially sensitive patterns from response
        
        Args:
            text: Response text
            
        Returns:
            Redacted text
        """
        # Redact email-like patterns
        import re
        text = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[EMAIL]", text)
        
        # Redact phone patterns
        text = re.sub(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b", "[PHONE]", text)
        
        return text
