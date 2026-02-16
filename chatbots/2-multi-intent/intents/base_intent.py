"""
Base class for all intent handlers
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


class BaseIntent(ABC):
    """Abstract base class for intent handlers"""
    
    def __init__(self, state: Dict[str, Any], bedrock_client):
        """
        Initialize intent handler
        
        Args:
            state: Current state for this intent
            bedrock_client: Bedrock client for LLM calls
        """
        self.state = state
        self.bedrock_client = bedrock_client
        self.logger = logging.getLogger(self.__class__.__name__)
        self.intent_type = self.__class__.__name__.lower().replace("intent", "")
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return system prompt specific to this intent"""
        pass
    
    @abstractmethod
    def extract_parameters(self, user_message: str) -> Dict[str, Any]:
        """
        Extract parameters from user message
        
        Returns:
            Dict with extracted parameters
        """
        pass
    
    @abstractmethod
    def validate(self) -> Dict:
        """
        Validate extracted parameters
        
        Returns:
            Dict with validation results (valid: bool, missing: list)
        """
        pass
    
    @abstractmethod
    def execute(self) -> Dict:
        """
        Execute the intent logic
        
        Returns:
            Dict with execution results
        """
        pass
    
    @abstractmethod
    def respond(self, user_message: str, conversation_history: List[Dict]) -> str:
        """
        Generate response for the user
        
        Returns:
            Response string
        """
        pass
    
    def get_status(self) -> Dict:
        """Get current status of intent execution"""
        validation = self.validate()
        return {
            "intent": self.intent_type,
            "state": self.state,
            "validation": validation,
            "ready_to_execute": validation.get("valid", False)
        }
