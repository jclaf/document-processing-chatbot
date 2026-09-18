import os
from openai import OpenAI
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

def get_openrouter_client(api_key: Optional[str] = None) -> OpenAI:
    """Initialise et retourne le client OpenAI configuré pour OpenRouter."""
    key = api_key
    if not key:
        raise ValueError("La clé API OpenRouter est introuvable.")
    
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=key,
    )
    
def call_rag_openrouter(
    query: str, 
    retrieved_context: str,
    api_key: Optional[str] = None,
    model: str = os.getenv("MODEL_NAME")  # Remplacez par le nom du modèle que vous souhaitez utiliser
) -> str:
    """
    Interroge un modèle via OpenRouter pour l'agent RAG strict 
    garantissant la qualité et la conformité des sources.
    """
    try:
        client = get_openrouter_client(api_key or os.getenv("OPENROUTER_API_KEY"))
        
        system_prompt = (
            "Tu es un agent RAG strict axé sur la qualité et la conformité des données. "
            "Tu dois **uniquement** utiliser les faits présents dans le contexte fourni. "
            "Si le contexte ne permet pas de répondre avec certitude, réponds explicitement : "
            "'Information non disponible dans les sources conformes.' "
            "Cite obligatoirement la source (source_id) pour chaque affirmation."
        )
        
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Contexte :\n{retrieved_context}\n\nQuestion : {query}"}
            ],
            temperature=0.0
        )
        
        return completion.choices[0].message.content
    except Exception as e:
        return f"Erreur lors de l'appel à l'API OpenRouter : {str(e)}"