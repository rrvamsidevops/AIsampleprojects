"""Information/FAQ intent handler"""

import logging
from typing import Dict, List, Any
from .base_intent import BaseIntent


class InformationIntent(BaseIntent):
    """Handles information and FAQ requests"""
    
    def get_system_prompt(self) -> str:
        return """You are a helpful information specialist. Your role is to:
1. Answer customer questions about services, policies, hours, etc.
2. Provide accurate, helpful information
3. Offer to connect to specialist if needed
4. Suggest related services they might be interested in

Be informative, friendly, and concise."""
    
    def extract_parameters(self, user_message: str) -> Dict[str, Any]:
        """Extract information request parameters"""
        extraction_result = self.bedrock_client.extract_parameters(
            "information", user_message, []
        )
        
        for param_name, param_value in extraction_result.get("extracted", {}).items():
            self.state[param_name] = param_value
        
        self.logger.debug(f"Extracted info params: {extraction_result['extracted']}")
        return extraction_result["extracted"]
    
    def validate(self) -> Dict:
        """Validate information request"""
        # Information requests don't require parameters to be valid
        has_topic = "topic" in self.state or "question" in self.state
        
        return {
            "valid": True,
            "has_topic": has_topic,
            "message": "Ready to provide information"
        }
    
    def execute(self) -> Dict:
        """Execute information lookup"""
        # For this demo, just mark as handled
        self.state["status"] = "answered"
        
        self.logger.info(f"Information request handled for: {self.state.get('topic', 'general')}")
        return {
            "success": True,
            "message": "Information provided"
        }
    
    def respond(self, user_message: str, conversation_history: List[Dict]) -> str:
        """Generate informational response"""
        system_prompt = self.get_system_prompt()
        
        context = {
            "extracted_parameters": self.state,
            "validation_status": self.validate()
        }
        
        response = self.bedrock_client.generate_response(
            system_prompt,
            user_message,
            conversation_history,
            context
        )
        return response
