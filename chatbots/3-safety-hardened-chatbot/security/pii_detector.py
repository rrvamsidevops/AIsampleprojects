"""
PII (Personally Identifiable Information) detection and redaction module
"""

import logging
import re
from typing import Dict, List, Tuple

import config

logger = logging.getLogger(__name__)


class PIIDetector:
    """Detects and redacts Personally Identifiable Information"""
    
    # PII patterns
    PATTERNS = {
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "phone": r"\b(\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
        "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
        "credit_card": r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",
        "ipv4": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
        "url": r"https?://[^\s]+",
    }
    
    def __init__(self):
        self.compiled_patterns = {
            name: re.compile(pattern) for name, pattern in self.PATTERNS.items()
        }
    
    def detect(self, text: str) -> Dict[str, List[str]]:
        """
        Detect PII in text
        
        Args:
            text: Text to analyze
            
        Returns:
            Dict with PII types and matches
        """
        findings = {}
        
        for pii_type, pattern in self.compiled_patterns.items():
            matches = pattern.findall(text)
            if matches:
                findings[pii_type] = matches
                logger.warning(f"PII detected - {pii_type}: {len(matches)} occurrence(s)")
        
        return findings
    
    def redact(self, text: str) -> Tuple[str, Dict[str, List[str]]]:
        """
        Redact PII from text
        
        Args:
            text: Text to redact
            
        Returns:
            Tuple of (redacted_text, pii_findings)
        """
        redacted = text
        findings = {}
        
        # Email redaction
        email_matches = re.findall(self.PATTERNS["email"], redacted)
        if email_matches:
            findings["email"] = email_matches
            redacted = re.sub(self.PATTERNS["email"], "[EMAIL]", redacted)
        
        # Phone redaction
        phone_matches = re.findall(self.PATTERNS["phone"], redacted)
        if phone_matches:
            findings["phone"] = phone_matches
            redacted = re.sub(self.PATTERNS["phone"], "[PHONE]", redacted)
        
        # SSN redaction
        ssn_matches = re.findall(self.PATTERNS["ssn"], redacted)
        if ssn_matches:
            findings["ssn"] = ssn_matches
            redacted = re.sub(self.PATTERNS["ssn"], "[SSN]", redacted)
        
        # Credit card redaction
        cc_matches = re.findall(self.PATTERNS["credit_card"], redacted)
        if cc_matches:
            findings["credit_card"] = cc_matches
            redacted = re.sub(self.PATTERNS["credit_card"], "[CARD]", redacted)
        
        # URL redaction
        url_matches = re.findall(self.PATTERNS["url"], redacted)
        if url_matches:
            findings["url"] = url_matches
            redacted = re.sub(self.PATTERNS["url"], "[URL]", redacted)
        
        if findings:
            logger.warning(f"PII redacted: {findings}")
        
        return redacted, findings
