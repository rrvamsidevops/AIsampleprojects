"""
Configuration and constants for Multi-Intent Chatbot
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# AWS Configuration
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_PROFILE = os.getenv("AWS_PROFILE", "default")
BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "us.anthropic.claude-3-5-sonnet-20241022-v2:0")

# Model Parameters
MODEL_TEMPERATURE = 0.7
MODEL_MAX_TOKENS = 1000

# Intent Configuration
INTENT_TYPES = {
    "booking": {
        "name": "booking",
        "description": "User wants to book a service or product",
        "required_params": ["service_type", "date"],
        "optional_params": ["preferences", "special_requests"]
    },
    "cancellation": {
        "name": "cancellation",
        "description": "User wants to cancel an existing booking",
        "required_params": ["booking_id"],
        "optional_params": ["reason", "confirmation_needed"]
    },
    "refund": {
        "name": "refund",
        "description": "User wants a refund for a purchase or booking",
        "required_params": ["order_id"],
        "optional_params": ["amount", "reason"]
    },
    "information": {
        "name": "information",
        "description": "User is asking for information or FAQs",
        "required_params": [],
        "optional_params": ["topic", "context"]
    },
    "complaint": {
        "name": "complaint",
        "description": "User has a complaint about service or product",
        "required_params": ["issue_description"],
        "optional_params": ["booking_id", "severity", "resolution_wanted"]
    }
}

# Paths
PROJECT_ROOT = Path(__file__).parent
PROMPTS_DIR = PROJECT_ROOT / "prompts"
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = LOGS_DIR / "chatbot.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Conversation Settings
MAX_HISTORY_TURNS = 10  # Keep last N conversation turns
STATE_REFRESH_FREQUENCY = 3  # Update state every N turns

# Intent Switch Threshold
INTENT_CONFIDENCE_THRESHOLD = 0.7  # Min confidence to confirm intent switch
