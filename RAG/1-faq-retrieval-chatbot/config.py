import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    FAQ_DATA_PATH = os.getenv("FAQ_DATA_PATH", "data/faq.json")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_DIR = os.getenv("LOG_DIR", "logs")
