"""
Integration tests for Multi-Intent Chatbot (requires AWS)
"""

import pytest
import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import MultiIntentChatbot


class TestMultiIntentChatbotIntegration:
    """Integration tests with AWS Bedrock"""
    
    @pytest.fixture
    def chatbot(self):
        """Create chatbot instance for testing"""
        return MultiIntentChatbot()
    
    @pytest.mark.integration
    def test_chatbot_initialization(self, chatbot):
        """Test chatbot initializes correctly"""
        assert chatbot.bedrock_client is not None
        assert chatbot.state is not None
        assert len(chatbot.intent_classes) == 5
    
    @pytest.mark.integration
    def test_simple_booking_flow(self, chatbot):
        """Test simple booking conversation flow"""
        # First message
        response1 = chatbot.chat("I want to book a flight")
        assert response1 is not None
        assert len(response1) > 0
        
        # Second message
        response2 = chatbot.chat("For tomorrow")
        assert response2 is not None
        
        # Check state was updated
        assert chatbot.state.turn_count == 2
        assert chatbot.state.current_intent == "booking"
    
    @pytest.mark.integration
    def test_intent_classification(self, chatbot):
        """Test intent classification"""
        intent = chatbot.classify_intent("I want to book a flight")
        
        assert intent in chatbot.intent_classes
        assert intent == "booking"
    
    @pytest.mark.integration
    def test_intent_switching(self, chatbot):
        """Test switching between intents"""
        # Start with booking
        chatbot.chat("I want to book a flight")
        assert chatbot.state.current_intent == "booking"
        
        # Switch to cancellation
        chatbot.chat("Actually, cancel my booking ABC123")
        assert chatbot.state.current_intent == "cancellation"
        
        # Check intent history
        assert len(chatbot.state.intent_history) == 2
        assert chatbot.state.context["intent_switches_count"] == 1
    
    @pytest.mark.integration
    def test_information_request(self, chatbot):
        """Test information intent"""
        response = chatbot.chat("What are your business hours?")
        
        assert response is not None
        assert len(response) > 0
        assert chatbot.state.current_intent == "information"
    
    @pytest.mark.integration
    def test_complaint_handling(self, chatbot):
        """Test complaint intent"""
        response = chatbot.chat("I have a complaint about my booking")
        
        assert response is not None
        assert chatbot.state.current_intent == "complaint"
    
    @pytest.mark.integration
    def test_conversation_history(self, chatbot):
        """Test conversation history is maintained"""
        chatbot.chat("Hello")
        chatbot.chat("I want to book a flight")
        chatbot.chat("For tomorrow")
        
        history = chatbot.state.get_history_for_api()
        
        assert len(history) >= 3
        assert history[0]["role"] == "user"
        assert history[1]["role"] == "assistant"
    
    @pytest.mark.integration
    def test_conversation_summary(self, chatbot):
        """Test conversation summary generation"""
        chatbot.chat("I want to book a flight")
        chatbot.chat("Tomorrow")
        
        summary = chatbot.state.get_summary()
        
        assert summary["turn_count"] == 2
        assert summary["current_intent"] == "booking"
        assert len(summary["conversation_history"]) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "integration"])
