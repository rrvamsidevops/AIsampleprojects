"""
Jailbreak detection module
Identifies attempts to bypass safety guidelines
"""

import logging
from typing import Dict, Optional

import config

logger = logging.getLogger(__name__)


class JailbreakDetector:
    """Detects jailbreak and prompt injection attempts"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def detect(self, text: str) -> Optional[Dict]:
        """
        Detect jailbreak attempts
        
        Args:
            text: User message
            
        Returns:
            Dict with detection info or None if safe
        """
        # Check for role-playing attempts
        roleplay_match = self.detect_roleplay_jailbreak(text)
        if roleplay_match:
            return {
                "type": "roleplay",
                "pattern": roleplay_match,
                "severity": "high"
            }
        
        # Check for "do anything now" variants
        dan_match = self.detect_dan_variant(text)
        if dan_match:
            return {
                "type": "dan_variant",
                "pattern": dan_match,
                "severity": "high"
            }
        
        # Check for constraint removal attempts
        constraint_match = self.detect_constraint_removal(text)
        if constraint_match:
            return {
                "type": "constraint_removal",
                "pattern": constraint_match,
                "severity": "medium"
            }
        
        return None
    
    def detect_roleplay_jailbreak(self, text: str) -> Optional[str]:
        """
        Detect: "act as if", "roleplay as", "pretend to be"
        """
        patterns = [
            "act as if",
            "roleplay as",
            "pretend to be",
            "imagine you are",
            "suppose you are",
        ]
        
        text_lower = text.lower()
        for pattern in patterns:
            if pattern in text_lower:
                return pattern
        
        return None
    
    def detect_dan_variant(self, text: str) -> Optional[str]:
        """
        Detect: DAN, "do anything now", "unrestricted mode"
        """
        patterns = [
            "DAN",
            "do anything now",
            "STAN",
            "unrestricted",
            "jailbreak",
            "no restrictions",
        ]
        
        text_lower = text.lower()
        for pattern in patterns:
            if pattern.lower() in text_lower:
                return pattern
        
        return None
    
    def detect_constraint_removal(self, text: str) -> Optional[str]:
        """
        Detect: "ignore", "forget", "override" instructions
        """
        patterns = [
            "ignore your instructions",
            "forget your instructions",
            "override your instructions",
            "disable safety",
            "turn off safety",
        ]
        
        text_lower = text.lower()
        for pattern in patterns:
            if pattern in text_lower:
                return pattern
        
        return None
