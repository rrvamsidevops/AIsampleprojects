"""
Main Customer Support Chatbot Application
Built with AWS Bedrock (Claude 3.5 Sonnet)
"""

import json
import logging
import sys
from datetime import datetime
from typing import List, Dict, Optional

import config
from utils.bedrock_client import BedrockClient

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(config.LOG_FILE) if config.ENABLE_LOGGING else logging.NullHandler(),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class CustomerSupportChatbot:
    """Customer support chatbot using AWS Bedrock"""

    def __init__(self):
        """Initialize chatbot with Bedrock client and system prompt"""
        try:
            # Initialize Bedrock client
            self.bedrock_client = BedrockClient(
                model_id=config.BEDROCK_MODEL_ID,
                region=config.AWS_REGION,
                profile=config.AWS_PROFILE
            )
            
            # Load system prompt
            self.system_prompt = self._load_system_prompt()
            
            # Initialize conversation history
            self.conversation_history: List[Dict[str, str]] = []
            
            logger.info("Customer Support Chatbot initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize chatbot: {e}")
            raise

    def _load_system_prompt(self) -> str:
        """
        Load system prompt from file
        
        Returns:
            System prompt text
        """
        try:
            with open(config.SYSTEM_PROMPT_FILE, "r") as f:
                prompt = f.read().strip()
            logger.info("System prompt loaded successfully")
            return prompt
        except FileNotFoundError:
            logger.error(f"System prompt file not found: {config.SYSTEM_PROMPT_FILE}")
            raise

    def _trim_conversation_history(self) -> None:
        """Keep only recent conversation turns to manage context window"""
        if len(self.conversation_history) > config.MAX_CONVERSATION_HISTORY:
            # Keep only the most recent turns
            self.conversation_history = self.conversation_history[-config.MAX_CONVERSATION_HISTORY:]
            logger.debug(f"Trimmed conversation history to {len(self.conversation_history)} turns")

    def get_response(self, user_message: str) -> Optional[str]:
        """
        Get chatbot response to user message
        
        Args:
            user_message: User's message
            
        Returns:
            Chatbot response or None on error
        """
        try:
            # Validate input
            if not user_message or not user_message.strip():
                return config.ERROR_MESSAGES["invalid_input"]
            
            user_message = user_message.strip()
            
            # Log user message
            logger.info(f"User: {user_message}")
            
            # Format messages for API call
            messages = self.bedrock_client.format_messages(
                self.conversation_history,
                user_message
            )
            
            # Get response from Bedrock
            assistant_response = self.bedrock_client.invoke_model(
                messages=messages,
                system_prompt=self.system_prompt,
                temperature=config.MODEL_TEMPERATURE,
                max_tokens=config.MODEL_MAX_TOKENS,
                top_p=config.MODEL_TOP_P
            )
            
            if not assistant_response:
                logger.warning("Empty response from Bedrock")
                return config.ERROR_MESSAGES["bedrock_error"]
            
            # Log assistant response
            logger.info(f"Assistant: {assistant_response}")
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": assistant_response})
            
            # Trim history if needed
            self._trim_conversation_history()
            
            return assistant_response
            
        except Exception as e:
            logger.error(f"Error getting response: {e}")
            return config.ERROR_MESSAGES["bedrock_error"]

    def reset_conversation(self) -> None:
        """Reset conversation history"""
        self.conversation_history = []
        logger.info("Conversation history reset")

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """
        Get current conversation history
        
        Returns:
            List of message dicts
        """
        return self.conversation_history.copy()

    def save_conversation(self, filename: str) -> bool:
        """
        Save conversation to JSON file
        
        Args:
            filename: Output filename
            
        Returns:
            True if successful, False otherwise
        """
        try:
            data = {
                "timestamp": datetime.now().isoformat(),
                "conversation": self.conversation_history
            }
            
            with open(filename, "w") as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Conversation saved to {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save conversation: {e}")
            return False


def main():
    """Main chat loop"""
    print("\n" + "="*60)
    print("🤖 Customer Support Chatbot")
    print("="*60)
    print("Welcome to customer support! Type 'exit' to quit.\n")
    
    try:
        # Initialize chatbot
        chatbot = CustomerSupportChatbot()
        print("✓ Chatbot ready!\n")
        
        # Chat loop
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                # Check for exit command
                if user_input.lower() in ["exit", "quit", "bye"]:
                    print("\nThank you for contacting support. Goodbye!")
                    break
                
                # Check for special commands
                if user_input.lower() == "reset":
                    chatbot.reset_conversation()
                    print("✓ Conversation reset\n")
                    continue
                
                if user_input.lower() == "save":
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"conversation_{timestamp}.json"
                    if chatbot.save_conversation(filename):
                        print(f"✓ Conversation saved to {filename}\n")
                    continue
                
                if user_input.lower() == "history":
                    print("\n--- Conversation History ---")
                    for msg in chatbot.get_conversation_history():
                        role = msg["role"].upper()
                        print(f"{role}: {msg['content'][:100]}...")
                    print("---\n")
                    continue
                
                # Get response
                response = chatbot.get_response(user_input)
                if response:
                    print(f"\nSupport: {response}\n")
                else:
                    print(f"\nSupport: {config.ERROR_MESSAGES['bedrock_error']}\n")
                    
            except KeyboardInterrupt:
                print("\n\nChatbot interrupted.")
                break
            except Exception as e:
                logger.error(f"Error in chat loop: {e}")
                print(f"\nAn error occurred. Please try again.\n")
    
    except Exception as e:
        logger.error(f"Failed to start chatbot: {e}")
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
