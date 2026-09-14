"""
Configuration de l'application.
"""
import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Récupère le chemin absolu du dossier racine du projet (au-dessus de 'src')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")

# Crée le dossier logs s'il n'existe pas
os.makedirs(LOG_DIR, exist_ok=True)

class Config:
    """Configuration de base."""
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 5000))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


def setup_logging():
    """Configure le système de logging."""
    log_file_path = os.path.join(LOG_DIR, "chatbot.log")
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file_path),
            logging.StreamHandler()
        ]
    )