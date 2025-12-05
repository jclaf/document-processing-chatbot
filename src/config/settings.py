"""
Configuration de l'application.
"""

import os
import logging
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration de base."""
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 5000))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


def setup_logging():
    """Configure le système de logging."""
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("logs/chatbot.log"),
            logging.StreamHandler()
        ]
    )
