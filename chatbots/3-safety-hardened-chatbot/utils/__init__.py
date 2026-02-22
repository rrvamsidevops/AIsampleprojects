"""
Metrics tracking for safety-hardened chatbot
"""

import json
import logging
from pathlib import Path
from typing import Dict
from datetime import datetime

import config

logger = logging.getLogger(__name__)


class SafetyMetrics:
    """Tracks safety-related metrics"""
    
    def __init__(self):
        self.metrics = {
            "total_requests": 0,
            "blocked_requests": 0,
            "pii_detections": 0,
            "jailbreak_attempts": 0,
            "safety_violations": 0,
            "successful_responses": 0,
        }
    
    def record_request(self):
        """Record incoming request"""
        self.metrics["total_requests"] += 1
    
    def record_blocked(self):
        """Record blocked request"""
        self.metrics["blocked_requests"] += 1
    
    def record_pii_detection(self):
        """Record PII detection"""
        self.metrics["pii_detections"] += 1
    
    def record_jailbreak_attempt(self):
        """Record jailbreak attempt"""
        self.metrics["jailbreak_attempts"] += 1
    
    def record_safety_violation(self):
        """Record safety violation"""
        self.metrics["safety_violations"] += 1
    
    def record_success(self):
        """Record successful response"""
        self.metrics["successful_responses"] += 1
    
    def get_metrics(self) -> Dict:
        """Get current metrics"""
        return self.metrics.copy()
    
    def calculate_safety_score(self) -> float:
        """
        Calculate safety score (0-100)
        Higher = safer
        """
        if self.metrics["total_requests"] == 0:
            return 100.0
        
        safe_requests = self.metrics["total_requests"] - self.metrics["blocked_requests"]
        return (safe_requests / self.metrics["total_requests"]) * 100
    
    def save_metrics(self, filename: str = None):
        """Save metrics to file"""
        filename = filename or config.LOGS_DIR / "safety_metrics.json"
        
        try:
            data = {
                "timestamp": datetime.now().isoformat(),
                "metrics": self.metrics,
                "safety_score": self.calculate_safety_score()
            }
            
            with open(filename, "w") as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Metrics saved to {filename}")
        except Exception as e:
            logger.error(f"Failed to save metrics: {e}")
