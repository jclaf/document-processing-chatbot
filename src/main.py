"""
Point d'entrée principal du chatbot.
"""

import logging
from config.settings import setup_logging
from typing import Union

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from io import BytesIO
from pypdf import PdfReader
import os

from api_call import call_rag_openrouter

setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI(title="API Agent RAG Conformité", version="1.0")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, "docs")

# class QueryRequest(BaseModel):
#     query: str
#     api_key: str | None = None
#     file_name: str | None = Form(None)
#     file: UploadFile | None = File(None)  # Nom du fichier à utiliser comme contexte, si fourni

class QueryResponse(BaseModel):
    response: str
    source_used: str

@app.get("/")
def read_root() -> dict[str, str]:
    """Point d'entrée racine de l'API."""
    return {"message": "Bienvenue sur l'API de l'Agent RAG Data Quality !"}

@app.post("/ask", response_model=QueryResponse)
async def ask_rag(
    query: str = Form(...),
    api_key: str | None = Form(None),
    file_name: str | None = Form(None),
    file: UploadFile | None = File(None)):
    """Endpoint pour poser une question à l'agent RAG."""
    try:
        # Clé API récupérée soit de la requête, soit des variables d'environnement du serveur
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise HTTPException(status_code=400, detail="Clé API OpenRouter manquante.")
        file_content = ""
        source_id = "default_context"

        if file and file.filename:
            source_id = file.filename
            try:
                contents = await file.read()
                if file.filename.lower().endswith(".pdf"):
                    pdf_file = BytesIO(contents)
                    reader = PdfReader(pdf_file)
                    text_pages = [page.extract_text() for page in reader.pages if page.extract_text()]
                    file_content = "\n".join(text_pages)
                else:
                    file_content = contents.decode("utf-8")
            except Exception as e:
                file_content = f"Erreur lors de la lecture du fichier uploadé en mémoire : {str(e)}"

        # 2. Si un fichier a été demandé ou sélectionné depuis le dossier docs
        elif file_name:
            source_id = file_name
            file_path = os.path.join(DOCS_DIR, file_name)
            if os.path.exists(file_path):
                try:
                    if file_name.lower().endswith(".pdf"):
                        reader = PdfReader(file_path)
                        text_pages = [page.extract_text() for page in reader.pages if page.extract_text()]
                        file_content = "\n".join(text_pages)
                    else:
                        with open(file_path, "r", encoding="utf-8") as f:
                            file_content = f.read()
                except Exception:
                    file_content = "Erreur de lecture du fichier depuis le dossier docs."
            else:
                file_content = f"Fichier '{file_name}' introuvable dans le dossier docs."
        # Si aucun fichier spécifique n'est trouvé ou demandé, on cherche par défaut dans les fichiers du dossier docs
        if not file_content and os.path.exists(DOCS_DIR):
            doc_files = os.listdir(DOCS_DIR)
            if doc_files:
                # On prend le premier fichier disponible dans 'docs' comme source par défaut
                default_file = doc_files[0]
                source_id = default_file
                file_path = os.path.join(DOCS_DIR, default_file)
                try:
                    if default_file.lower().endswith(".pdf"):
                        reader = PdfReader(file_path)
                        text_pages = [page.extract_text() for page in reader.pages if page.extract_text()]
                        file_content = "\n".join(text_pages)
                    else:
                        with open(file_path, "r", encoding="utf-8") as f:
                            file_content = f.read()
                except Exception:
                    file_content = "Erreur de lecture du fichier par défaut."
        # Fallback ultime si le dossier docs est vide
        if not file_content:
            source_id = os.getenv("DEFAULT_FILE_NAME")
            file_content = (
                "Les données ne doivent pas être conservées indéfiniment en base active. "
                "Elles doivent être détruites, anonymisées ou archivées dans le respect des obligations légales."
            )
        # Contexte simulé basé sur vos documents conformes (à brancher sur votre base vectorielle plus tard)
        # Construction du contexte strict pour l'agent RAG
        retrieved_context = (
            f"[source_id: {source_id} | Statut: Validé]\n"
            f"{file_content}"
        )

        # Appel à la fonction OpenRouter
        response_text = call_rag_openrouter(
            query=query,
            retrieved_context=retrieved_context,
            api_key=api_key
        )

        return QueryResponse(response=response_text, source_used=f"../docs/{source_id}")

    except Exception as e:
        logger.error(f"Erreur dans /ask : {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))