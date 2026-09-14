import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


st.set_page_config(
    page_title="Agent RAG - Data Quality & Conformité",
    page_icon="🛡️",
    layout="centered"
)
    
st.title("🛡️ Agent RAG : Conformité & Data Quality")
st.markdown("Posez vos questions sur vos documents validés. Cet agent garantit la traçabilité des sources.")

# Configuration de la clé OpenRouter dans la barre latérale si non définie en variable d'environnement
with st.sidebar:
    st.header("Paramètres")
    api_key_input = st.text_input("Clé API OpenRouter", type="password", value=os.getenv("OPENROUTER_API_KEY", ""))
    api_url = st.text_input("URL de l'API FastAPI", value="http://127.0.0.1:8000/ask")
    st.divider()
    st.header("📁 Documents & Sources")
    uploaded_file = st.file_uploader(
        "Ajouter un document ou une capture d'écran", 
        type=["pdf", "txt", "md", "png", "jpg", "jpeg"]
    )
    if uploaded_file is None:
        if "uploaded_file_name" in st.session_state:
            del st.session_state["uploaded_file_name"]
    
    files = None
    if uploaded_file is not None:
        st.success(f"Fichier chargé : `{uploaded_file.name}`")
        # Vous pouvez stocker le contenu ou le fichier dans la session Streamlit si besoin
        st.session_state["uploaded_file_name"] = uploaded_file.name
        st.session_state["uploaded_file_bytes"] = uploaded_file.getvalue()
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
    
    if api_key_input:
        os.environ["OPENROUTER_API_KEY"] = api_key_input
    
    st.info(f"Modèle utilisé : {os.getenv('MODEL_NAME', 'Inconnu')} (Température : 0.0)")
    
    
# Initialisation de l'historique du chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des messages précédents
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
# Entrée utilisateur
if prompt := st.chat_input("Votre question sur les sources conformes..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        
        st.markdown("L'agent RAG est en train de générer une réponse basée sur les sources conformes...")
        #with st.spinner("Recherche dans les sources validées et génération..."):
        try:
            # Appel de l'API FastAPI
            payload = {
                "query": prompt,
                "api_key": api_key_input if api_key_input else None,
                "file_name": st.session_state.get("uploaded_file_name", None)
            }
            res = requests.post(api_url, data=payload, files=files, timeout=30)
            
            if res.status_code == 200:
                data = res.json()
                response_text = data.get("response")
            else:
                response_text = f"Erreur API ({res.status_code}) : {res.json().get('detail', 'Erreur inconnue')}"
        
        except requests.exceptions.ConnectionError:
            response_text = "⚠️ Impossible de se connecter au backend FastAPI. Assurez-vous qu'il est bien lancé."
        except Exception as e:
            response_text = f"Erreur technique : {str(e)}"
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        st.markdown(response_text)
