"""Booking intent handler"""

import logging
from typing import Dict, List, Any
from .base_intent import BaseIntent
import json


class BookingIntent(BaseIntent):
    """Handles booking requests"""
    
    def get_system_prompt(self) -> str:
        return """You are a helpful booking assistant. Your role is to:
1. Understand what the customer wants to book (flights, hotels, events, etc.)
2. Gather required information (dates, preferences, special requests)
3. Confirm all details before booking
4. Provide booking confirmation with reference number

Be professional, friendly, and thorough. Ask clarifying questions if needed.
Keep responses concise and actionable."""
    
    def extract_parameters(self, user_message: str) -> Dict[str, Any]:
        """Extract booking parameters from user message"""
        # Use LLM for extraction
        extraction_result = self.bedrock_client.extract_parameters(
            "booking", user_message, []
        )
        
        for param_name, param_value in extraction_result.get("extracted", {}).items():
            self.state[param_name] = param_value
        
        self.logger.debug(f"Extracted booking params: {extraction_result['extracted']}")
        return extraction_result["extracted"]
    
    def validate(self) -> Dict:
        """Validate booking has required parameters"""
        required = ["service_type", "date"]
        present = [p for p in required if p in self.state]
        missing = [p for p in required if p not in self.state]
        
        is_valid = len(missing) == 0
        
        return {
            "valid": is_valid,
            "present": present,
            "missing": missing,
            "message": "Booking ready to confirm" if is_valid else f"Missing: {', '.join(missing)}"
        }
    
    def execute(self) -> Dict:
        """Execute the booking"""
        validation = self.validate()
        if not validation["valid"]:
            return {
                "success": False,
                "error": validation["message"]
            }
        
        # Mock booking execution
        booking_id = f"BK-{abs(hash(str(self.state))) % 10000000:07d}"
        self.state["booking_id"] = booking_id
        self.state["status"] = "confirmed"
        
        self.logger.info(f"Booking executed: {booking_id}")
        return {
            "success": True,
            "booking_id": booking_id,
            "message": f"Your booking {booking_id} has been confirmed!"
        }
    
    def respond(self, user_message: str, conversation_history: List[Dict]) -> str:
        """Generate booking response"""
        system_prompt = self.get_system_prompt()
        
        # Add current state to context
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
