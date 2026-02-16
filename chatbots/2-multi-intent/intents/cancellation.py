"""Cancellation intent handler"""

import logging
from typing import Dict, List, Any
from .base_intent import BaseIntent


class CancellationIntent(BaseIntent):
    """Handles cancellation requests"""
    
    def get_system_prompt(self) -> str:
        return """You are a cancellation specialist. Your role is to:
1. Understand what booking they want to cancel
2. Verify the booking ID or reference number
3. Confirm the cancellation is requested
4. Explain any cancellation fees or policies
5. Process the cancellation if confirmed

Be empathetic and professional. Try to understand why they want to cancel."""
    
    def extract_parameters(self, user_message: str) -> Dict[str, Any]:
        """Extract cancellation parameters"""
        extraction_result = self.bedrock_client.extract_parameters(
            "cancellation", user_message, []
        )
        
        for param_name, param_value in extraction_result.get("extracted", {}).items():
            self.state[param_name] = param_value
        
        self.logger.debug(f"Extracted cancellation params: {extraction_result['extracted']}")
        return extraction_result["extracted"]
    
    def validate(self) -> Dict:
        """Validate cancellation has booking ID"""
        has_booking_id = "booking_id" in self.state
        has_confirmation = "confirmation" in self.state and self.state["confirmation"] == "yes"
        
        is_valid = has_booking_id and has_confirmation
        
        return {
            "valid": is_valid,
            "has_booking_id": has_booking_id,
            "has_confirmation": has_confirmation,
            "message": "Ready to cancel" if is_valid else "Need booking ID and confirmation"
        }
    
    def execute(self) -> Dict:
        """Execute the cancellation"""
        validation = self.validate()
        if not validation["valid"]:
            return {
                "success": False,
                "error": validation["message"]
            }
        
        # Mock cancellation
        booking_id = self.state.get("booking_id")
        self.state["status"] = "cancelled"
        self.state["cancellation_timestamp"] = "2024-02-15T10:30:00Z"
        
        self.logger.info(f"Cancellation processed: {booking_id}")
        return {
            "success": True,
            "booking_id": booking_id,
            "message": f"Booking {booking_id} has been cancelled successfully."
        }
    
    def respond(self, user_message: str, conversation_history: List[Dict]) -> str:
        """Generate cancellation response"""
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
