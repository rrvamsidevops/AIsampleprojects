"""
Unit tests for Multi-Intent Chatbot
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import INTENT_TYPES
from utils.state_manager import ConversationState
from intents import (
    BookingIntent, CancellationIntent, RefundIntent,
    InformationIntent, ComplaintIntent
)


class MockBedrockClient:
    """Mock Bedrock client for testing"""
    
    def __init__(self):
        pass
    
    def extract_parameters(self, intent_type, user_message, history):
        """Mock parameter extraction"""
        return {
            "extracted": {
                "service_type": "flight",
                "date": "tomorrow",
                "booking_id": "ABC123",
                "order_id": "XYZ789"
            },
            "missing": [],
            "confidence": 0.9
        }
    
    def generate_response(self, system_prompt, user_message, history, context=None):
        """Mock response generation"""
        return f"Mock response for {context.get('extracted_parameters', {}) if context else {}}."


class TestConversationState:
    """Test conversation state management"""
    
    def test_initialization(self):
        """Test state initializes correctly"""
        state = ConversationState()
        assert state.turn_count == 0
        assert state.current_intent is None
        assert len(state.conversation_history) == 0
    
    def test_add_message(self):
        """Test adding messages to history"""
        state = ConversationState()
        state.add_message("user", "Hello")
        
        assert state.turn_count == 1
        assert len(state.conversation_history) == 1
        assert state.conversation_history[0]["role"] == "user"
    
    def test_set_current_intent(self):
        """Test setting and tracking intent switches"""
        state = ConversationState()
        
        # First intent
        result = state.set_current_intent("booking")
        assert result == True
        assert state.current_intent == "booking"
        
        # Same intent
        result = state.set_current_intent("booking")
        assert result == False
        
        # New intent
        result = state.set_current_intent("cancellation")
        assert result == True
        assert state.current_intent == "cancellation"
        assert len(state.intent_history) == 2
    
    def test_intent_state_management(self):
        """Test per-intent state storage"""
        state = ConversationState()
        
        state.update_intent_state("booking", "date", "2024-02-20")
        state.update_intent_state("booking", "service_type", "flight")
        
        intent_state = state.get_intent_state("booking")
        assert intent_state["date"] == "2024-02-20"
        assert intent_state["service_type"] == "flight"
    
    def test_validate_intent_state(self):
        """Test intent state validation"""
        state = ConversationState()
        state.update_intent_state("booking", "date", "tomorrow")
        
        required = ["date", "service_type"]
        validation = state.validate_intent_state("booking", required)
        
        assert "date" in validation["present"]
        assert "service_type" in validation["missing"]
        assert not validation["is_valid"]
    
    def test_state_refresh_check(self):
        """Test state refresh frequency check"""
        state = ConversationState()
        
        # Add messages up to refresh frequency
        for i in range(3):
            state.add_message("user", f"Message {i}")
        
        # Should refresh after 3 turns (configured in config)
        assert state.should_refresh_state()


class TestIntentHandlers:
    """Test intent handler classes"""
    
    def setup_method(self):
        """Setup for each test"""
        self.mock_client = MockBedrockClient()
    
    def test_booking_intent_initialization(self):
        """Test booking intent initializes correctly"""
        handler = BookingIntent({}, self.mock_client)
        
        assert handler.intent_type == "booking"
        assert handler.state == {}
    
    def test_booking_intent_validation(self):
        """Test booking intent parameter validation"""
        state = {"service_type": "flight"}
        handler = BookingIntent(state, self.mock_client)
        
        validation = handler.validate()
        
        assert not validation["valid"]
        assert "date" in validation["missing"]
        assert "service_type" in validation["present"]
    
    def test_booking_intent_execution(self):
        """Test booking intent execution"""
        state = {
            "service_type": "flight",
            "date": "tomorrow"
        }
        handler = BookingIntent(state, self.mock_client)
        
        result = handler.execute()
        
        assert result["success"]
        assert "booking_id" in result
        assert handler.state["status"] == "confirmed"
    
    def test_cancellation_intent_validation(self):
        """Test cancellation intent validation"""
        state = {"booking_id": "ABC123"}
        handler = CancellationIntent(state, self.mock_client)
        
        validation = handler.validate()
        
        assert not validation["valid"]
        assert not validation["has_confirmation"]
    
    def test_refund_intent_validation(self):
        """Test refund intent validation"""
        state = {"order_id": "XYZ789", "reason": "defective"}
        handler = RefundIntent(state, self.mock_client)
        
        validation = handler.validate()
        
        assert validation["valid"]
    
    def test_information_intent_validation(self):
        """Test information intent validation"""
        state = {}
        handler = InformationIntent(state, self.mock_client)
        
        validation = handler.validate()
        
        assert validation["valid"]
    
    def test_complaint_intent_validation(self):
        """Test complaint intent validation"""
        state = {"issue_description": "Wrong item received"}
        handler = ComplaintIntent(state, self.mock_client)
        
        validation = handler.validate()
        
        assert validation["valid"]


class TestConfigIntents:
    """Test intent configuration"""
    
    def test_all_intents_defined(self):
        """Test that all required intents are defined"""
        required_intents = ["booking", "cancellation", "refund", "information", "complaint"]
        
        for intent in required_intents:
            assert intent in INTENT_TYPES
            assert "name" in INTENT_TYPES[intent]
            assert "description" in INTENT_TYPES[intent]
            assert "required_params" in INTENT_TYPES[intent]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
