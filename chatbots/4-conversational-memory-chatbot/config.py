import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

class Config:
    """Centralized configuration for the chatbot."""
    # LLM provider settings
    PROVIDER = os.getenv("PROVIDER", "bedrock")
    MODEL = os.getenv("MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0")

    # Memory settings
    MEMORY_TYPE = os.getenv("MEMORY_TYPE", "short-term")  # 'short-term' or 'long-term'
    MEMORY_WINDOW = int(os.getenv("MEMORY_WINDOW", 5))  # Number of turns to remember

    # AWS credentials (if using Bedrock)
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    AWS_PROFILE = os.getenv("AWS_PROFILE", "default")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_DIR = os.getenv("LOG_DIR", "logs")

    # Other settings
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
