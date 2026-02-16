"""Refund intent handler"""

import logging
from typing import Dict, List, Any
from .base_intent import BaseIntent


class RefundIntent(BaseIntent):
    """Handles refund requests"""
    
    def get_system_prompt(self) -> str:
        return """You are a refund specialist. Your role is to:
1. Understand why customer wants a refund
2. Verify the order/booking ID and purchase details
3. Check refund eligibility based on policies
4. Calculate refund amount if applicable
5. Process refund with confirmation number

Be understanding but thorough. Explain policies clearly."""
    
    def extract_parameters(self, user_message: str) -> Dict[str, Any]:
        """Extract refund parameters"""
        extraction_result = self.bedrock_client.extract_parameters(
            "refund", user_message, []
        )
        
        for param_name, param_value in extraction_result.get("extracted", {}).items():
            self.state[param_name] = param_value
        
        self.logger.debug(f"Extracted refund params: {extraction_result['extracted']}")
        return extraction_result["extracted"]
    
    def validate(self) -> Dict:
        """Validate refund has order ID"""
        has_order_id = "order_id" in self.state
        has_reason = "reason" in self.state
        is_eligible = self.state.get("eligible", False)
        
        is_valid = has_order_id and has_reason
        
        return {
            "valid": is_valid,
            "has_order_id": has_order_id,
            "has_reason": has_reason,
            "is_eligible": is_eligible,
            "message": "Ready to process refund" if is_valid else "Need order ID and reason"
        }
    
    def execute(self) -> Dict:
        """Execute the refund"""
        validation = self.validate()
        if not validation["valid"]:
            return {
                "success": False,
                "error": validation["message"]
            }
        
        # Mock refund processing
        order_id = self.state.get("order_id")
        amount = float(self.state.get("amount", 0))
        refund_id = f"REF-{abs(hash(order_id)) % 10000000:07d}"
        
        self.state["status"] = "refunded"
        self.state["refund_id"] = refund_id
        self.state["refund_amount"] = amount
        
        self.logger.info(f"Refund processed: {refund_id}")
        return {
            "success": True,
            "order_id": order_id,
            "refund_id": refund_id,
            "amount": amount,
            "message": f"Refund {refund_id} for ${amount:.2f} has been processed."
        }
    
    def respond(self, user_message: str, conversation_history: List[Dict]) -> str:
        """Generate refund response"""
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
