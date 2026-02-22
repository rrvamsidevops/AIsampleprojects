"""
Main Multi-Intent Chatbot Application
"""

import logging
import sys
from typing import Optional
from utils.bedrock_client import BedrockClient
from utils.state_manager import ConversationState
from intents import (
    BookingIntent, CancellationIntent, RefundIntent, 
    InformationIntent, ComplaintIntent
)
import config


# Configure logging
logging.basicConfig(
    level=config.LOG_LEVEL,
    format=config.LOG_FORMAT,
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class MultiIntentChatbot:
    """Multi-intent chatbot with state management and routing"""
    
    def __init__(self):
        """Initialize the chatbot"""
        self.bedrock_client = BedrockClient()
        self.state = ConversationState()
        
        # Intent handler classes
        self.intent_classes = {
            "booking": BookingIntent,
            "cancellation": CancellationIntent,
            "refund": RefundIntent,
            "information": InformationIntent,
            "complaint": ComplaintIntent
        }
        
        # Current intent handler instance
        self.current_handler = None
        
        logger.info("MultiIntentChatbot initialized")
    
    def classify_intent(self, user_message: str) -> str:
        """
        Classify user message to determine intent
        
        Returns:
            Intent name (booking, cancellation, etc.)
        """
        logger.debug(f"Classifying intent for: {user_message[:50]}...")
        
        classification = self.bedrock_client.classify_intent(
            user_message,
            self.state.get_history_for_api()
        )
        
        intent = classification.get("intent", "information")
        confidence = classification.get("confidence", 0)
        
        logger.info(f"Intent: {intent} (confidence: {confidence:.2f})")
        
        # Extract any parameters identified during classification
        for param_name, param_value in classification.get("extracted_params", {}).items():
            self.state.update_intent_state(intent, param_name, param_value)
        
        return intent
    
    def get_intent_handler(self, intent: str):
        """Get or create intent handler for given intent"""
        if intent not in self.intent_classes:
            logger.warning(f"Unknown intent: {intent}, defaulting to information")
            intent = "information"
        
        # Get handler class
        handler_class = self.intent_classes[intent]
        
        # Get or initialize state for this intent
        intent_state = self.state.get_intent_state(intent)
        
        # Create handler instance
        handler = handler_class(intent_state, self.bedrock_client)
        return handler
    
    def handle_intent_switch(self, old_intent: Optional[str], new_intent: str) -> str:
        """
        Handle switching between intents
        
        Returns:
            Transitional message for the user
        """
        if old_intent is None:
            logger.info(f"Starting with intent: {new_intent}")
            return f"I understand you need help with {new_intent}. Let me assist you.\n"
        
        if old_intent == new_intent:
            return ""  # No switch, no message needed
        
        logger.info(f"Intent switch: {old_intent} → {new_intent}")
        
        # Clear the old intent state
        self.state.clear_intent_state(old_intent)
        
        return f"I see you want to switch to {new_intent}. Let me help you with that.\n"
    
    def chat(self, user_message: str) -> str:
        """
        Process user message and generate response
        
        Args:
            user_message: User's input
        
        Returns:
            Chatbot response
        """
        # Add user message to history
        self.state.add_message("user", user_message)
        
        try:
            # Classify intent
            intent = self.classify_intent(user_message)
            
            # Handle intent switching
            old_intent = self.state.current_intent
            switch_message = ""
            if self.state.set_current_intent(intent):
                switch_message = self.handle_intent_switch(old_intent, intent)
            
            # Get appropriate intent handler
            handler = self.get_intent_handler(intent)
            self.current_handler = handler
            
            # Extract parameters from user message
            handler.extract_parameters(user_message)
            
            # Validate extracted parameters
            validation = handler.validate()
            logger.debug(f"Validation: {validation}")
            
            # Generate response using handler
            response = handler.respond(
                user_message,
                self.state.get_history_for_api()
            )
            
            # Add response to history
            self.state.add_message("assistant", response)
            
            # Log conversation state
            if self.state.should_refresh_state():
                logger.debug(f"State summary: {self.state.get_summary()}")
            
            return switch_message + response
            
        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
            error_response = "I apologize, but I encountered an error processing your request. Please try again."
            self.state.add_message("assistant", error_response)
            return error_response
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the conversation"""
        summary = self.state.get_summary()
        
        output = "\n" + "="*60 + "\n"
        output += "CONVERSATION SUMMARY\n"
        output += "="*60 + "\n"
        output += f"Total turns: {summary['turn_count']}\n"
        output += f"Current intent: {summary['current_intent']}\n"
        output += f"Intent history: {' → '.join(summary['intent_history'])}\n"
        output += f"Intent switches: {summary['context']['intent_switches_count']}\n"
        output += "\nPer-Intent State:\n"
        
        for intent_name, state in summary['intent_states'].items():
            if state:
                output += f"  {intent_name}: {state}\n"
        
        output += "="*60 + "\n"
        return output
    
    def run_interactive(self):
        """Run interactive chatbot session"""
        print("\n" + "="*60)
        print("Multi-Intent Chatbot")
        print("="*60)
        print("I can help you with: booking, cancellation, refund, information, or complaints")
        print("Commands: 'exit' or 'quit' to end, 'summary' for conversation summary")
        print("="*60 + "\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ("quit", "exit", "bye", "goodbye"):
                    print("\nThank you for using Multi-Intent Chatbot. Goodbye!")
                    break
                
                if user_input.lower() == "summary":
                    print(self.get_conversation_summary())
                    continue
                
                response = self.chat(user_input)
                print(f"\nAssistant: {response}\n")
                
            except KeyboardInterrupt:
                print("\n\nSession ended by user.")
                break
            except Exception as e:
                logger.error(f"Unexpected error: {e}", exc_info=True)
                print(f"Error: {e}")


def main():
    """Main entry point"""
    try:
        chatbot = MultiIntentChatbot()
        chatbot.run_interactive()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
