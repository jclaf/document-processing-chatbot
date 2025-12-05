"""
Point d'entrée principal du chatbot.
"""

import logging
from config.settings import setup_logging
from typing import Union

from fastapi import FastAPI
from streamlit import run as streamlit_run
app = FastAPI()

@app.get("/")
def read_root() -> dict[str, str]:
    """Point d'entrée racine de l'API."""
    return {"message": "Bienvenue dans le chatbot!"}


def main():
    """Lance l'application chatbot."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Démarrage du chatbot...")
    
    # TODO: Initialiser et lancer le serveur


if __name__ == "__main__":
    main()
