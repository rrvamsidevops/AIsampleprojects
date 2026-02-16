"""Complaint intent handler"""

import logging
from typing import Dict, List, Any
from .base_intent import BaseIntent


class ComplaintIntent(BaseIntent):
    """Handles customer complaints"""
    
    def get_system_prompt(self) -> str:
        return """You are a customer care specialist handling complaints. Your role is to:
1. Listen and acknowledge the customer's complaint
2. Understand the issue and impact on them
3. Document the complaint properly
4. Offer solutions or escalate if needed
5. Follow up and ensure satisfaction

Be empathetic, professional, and solution-focused. Take complaints seriously."""
    
    def extract_parameters(self, user_message: str) -> Dict[str, Any]:
        """Extract complaint details"""
        extraction_result = self.bedrock_client.extract_parameters(
            "complaint", user_message, []
        )
        
        for param_name, param_value in extraction_result.get("extracted", {}).items():
            self.state[param_name] = param_value
        
        self.logger.debug(f"Extracted complaint params: {extraction_result['extracted']}")
        return extraction_result["extracted"]
    
    def validate(self) -> Dict:
        """Validate complaint has issue description"""
        has_issue = "issue_description" in self.state
        
        return {
            "valid": has_issue,
            "has_issue_description": has_issue,
            "message": "Complaint documented" if has_issue else "Need issue description"
        }
    
    def execute(self) -> Dict:
        """Execute complaint handling"""
        validation = self.validate()
        if not validation["valid"]:
            return {
                "success": False,
                "error": validation["message"]
            }
        
        # Mock complaint processing
        ticket_id = f"TKT-{abs(hash(self.state.get('issue_description', ''))) % 10000000:07d}"
        severity = self.state.get("severity", "normal")
        
        self.state["status"] = "opened"
        self.state["ticket_id"] = ticket_id
        self.state["severity"] = severity
        
        self.logger.info(f"Complaint ticket opened: {ticket_id}")
        return {
            "success": True,
            "ticket_id": ticket_id,
            "severity": severity,
            "message": f"Complaint ticket {ticket_id} has been opened. Our team will review and follow up."
        }
    
    def respond(self, user_message: str, conversation_history: List[Dict]) -> str:
        """Generate complaint response"""
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
