"""
app.py - Interface Streamlit pour le chatbot Dataiku

Chatbot conversationnel pour créer des workflows Dataiku avec Claude AI.
"""

import os
import sys
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

# Charge les variables d'environnement
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)
else:
    # Essaie de charger depuis le parent
    load_dotenv(Path(__file__).parents[1] / ".env")

# Ajoute src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from chat_handler import create_chat_handler
from dataiku_connector import get_connector


# Configuration de la page
st.set_page_config(
    page_title="Dataiku Workflow Creator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styles CSS personnalisés
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .dataset-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .stChatMessage {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialise l'état de session Streamlit"""
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "chat_handler" not in st.session_state:
        project_key = os.getenv("DSS_PROJECT_KEY", "TEST_WORKFLOW")
        try:
            st.session_state.chat_handler = create_chat_handler(project_key)
            st.session_state.project_key = project_key
        except Exception as e:
            st.error(f"Erreur d'initialisation : {e}")
            st.stop()

    if "connector" not in st.session_state:
        try:
            st.session_state.connector = get_connector(st.session_state.project_key)
        except Exception as e:
            st.error(f"Erreur de connexion Dataiku : {e}")
            st.stop()


def render_sidebar():
    """Affiche la sidebar avec les informations du projet"""
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")

        # Informations du projet
        st.info(f"**Projet:** {st.session_state.project_key}")

        # Bouton pour voir les datasets
        if st.button("📊 Voir les datasets disponibles", use_container_width=True):
            with st.spinner("Chargement des datasets..."):
                datasets = st.session_state.connector.get_available_datasets()

            st.markdown("---")
            st.markdown(f"### 📂 Datasets ({len(datasets)})")

            for ds in datasets:
                try:
                    info = st.session_state.connector.get_dataset_info(ds)
                    with st.expander(f"📄 {ds}"):
                        st.markdown(f"**{info['nb_columns']} colonnes:**")
                        for col in info['columns'][:10]:
                            st.text(f"  • {col['name']} ({col['type']})")
                        if len(info['columns']) > 10:
                            st.text(f"  ... +{len(info['columns']) - 10} colonnes")
                except Exception as e:
                    st.error(f"Erreur: {e}")

        st.markdown("---")

        # Bouton pour réinitialiser la conversation
        if st.button("🗑️ Nouvelle conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

        st.markdown("---")

        # Informations de connexion
        st.markdown("### 🔗 Connexion")
        dss_url = os.getenv("DSS_URL", "Non configuré")
        st.text(f"DSS: {dss_url[:40]}...")

        # Statistiques de la conversation
        st.markdown("---")
        st.markdown("### 📊 Statistiques")
        st.metric("Messages", len(st.session_state.messages))

        # Guide d'utilisation
        st.markdown("---")
        st.markdown("### 💡 Guide rapide")
        st.markdown("""
        **Exemples de requêtes:**

        • "Crée un workflow qui agrège les ventes par région"

        • "Je veux joindre healthcare_dataset avec Original_data sur patient_id"

        • "Nettoie les données de healthcare_dataset en supprimant les nulls"
        """)


def render_chat():
    """Affiche l'interface de chat"""
    # En-tête
    st.markdown('<div class="main-header">🤖 Dataiku Workflow Creator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Créez des workflows Dataiku en conversant avec Claude AI</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Affiche l'historique des messages
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]

        # Extrait le texte du contenu
        if isinstance(content, list):
            # Claude API format (avec blocks)
            text = ""
            for block in content:
                if hasattr(block, "text"):
                    text += block.text
                elif isinstance(block, dict) and "text" in block:
                    text += block["text"]
            content = text

        with st.chat_message(role):
            st.markdown(content)

    # Message d'accueil initial
    if len(st.session_state.messages) == 0:
        with st.chat_message("assistant"):
            st.markdown("""
            👋 Bonjour ! Je suis votre assistant pour créer des workflows Dataiku.

            **Comment puis-je vous aider ?**

            Je peux :
            - Analyser vos datasets disponibles
            - Vous aider à concevoir un workflow
            - Créer automatiquement des recettes (Python, Grouping, Join, etc.)
            - Générer le workflow complet dans DSS

            💬 **Commencez par me dire ce que vous voulez faire !**

            Exemple : *"Je veux créer un workflow qui agrège healthcare_dataset par patient"*
            """)

    # Input utilisateur
    if prompt := st.chat_input("Décrivez le workflow que vous souhaitez créer..."):
        # Affiche le message utilisateur
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Génère et affiche la réponse
        with st.chat_message("assistant"):
            with st.spinner("Claude réfléchit..."):
                try:
                    response_text, updated_history = st.session_state.chat_handler.process_message(
                        prompt,
                        st.session_state.messages
                    )

                    # Met à jour l'historique
                    st.session_state.messages = updated_history

                    # Affiche la réponse
                    st.markdown(response_text)

                except Exception as e:
                    st.error(f"❌ Erreur : {e}")
                    st.exception(e)


def main():
    """Point d'entrée principal de l'application"""
    # Vérifie les variables d'environnement requises
    required_env = ["ANTHROPIC_API_KEY", "DSS_URL", "DSS_API_KEY"]
    missing_env = [var for var in required_env if not os.getenv(var)]

    if missing_env:
        st.error(f"❌ Variables d'environnement manquantes : {', '.join(missing_env)}")
        st.info("📝 Créez un fichier `.env` avec ces variables. Voir `.env.example`")
        st.stop()

    # Initialise l'état de session
    init_session_state()

    # Affiche l'interface
    render_sidebar()
    render_chat()


if __name__ == "__main__":
    main()
