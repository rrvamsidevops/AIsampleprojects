"""
Configuration for Customer Support Chatbot
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# AWS Configuration
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_PROFILE = os.getenv("AWS_PROFILE", "default")

# Bedrock Configuration
BEDROCK_MODEL_ID = "anthropic.claude-3-5-sonnet-20241022-v2:0"
MODEL_TEMPERATURE = 0.7  # Balanced between deterministic and creative
MODEL_MAX_TOKENS = 1000  # Reasonable limit for support responses
MODEL_TOP_P = 0.95

# System Prompt Configuration
SYSTEM_PROMPT_FILE = "prompts/system_prompt.txt"

# Conversation Configuration
MAX_CONVERSATION_HISTORY = 10  # Keep last 10 turns in context
CONTEXT_WINDOW_BUFFER = 500  # Reserve tokens for response

# Logging Configuration
LOG_FILE = "logs/chatbot.log"
LOG_LEVEL = "INFO"

# Application Configuration
CHAT_TIMEOUT = 30  # Seconds to wait for Bedrock response
ENABLE_LOGGING = True

# Sample data paths
SAMPLE_INTERACTIONS_FILE = "data/sample_interactions.json"
EXAMPLES_FILE = "prompts/examples.json"

# API Configuration
BEDROCK_INVOKE_MODEL_ENDPOINT = f"bedrock-runtime.{AWS_REGION}.amazonaws.com"

# Error Messages
ERROR_MESSAGES = {
    "bedrock_error": "I'm experiencing technical difficulties. Please try again later.",
    "timeout": "The request took too long. Please try with a shorter message.",
    "invalid_input": "I couldn't understand that input. Could you rephrase?",
    "out_of_scope": "I'm a customer support assistant. I can help with account, billing, or technical issues related to our service.",
}

# Test conversation starters
TEST_CONVERSATIONS = [
    "I need help with my account",
    "How do I reset my password?",
    "I have a billing question",
    "The service isn't working properly",
    "Can I upgrade my plan?",
]
