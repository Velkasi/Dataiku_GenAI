#!/bin/bash
# Script de lancement du chatbot Dataiku

echo ""
echo "========================================"
echo " Dataiku Workflow Creator Chatbot"
echo "========================================"
echo ""

# Vérifie si .env existe
if [ ! -f .env ]; then
    echo "[ERREUR] Fichier .env manquant !"
    echo ""
    echo "Créez un fichier .env avec votre clé API Claude :"
    echo "  cp .env.example .env"
    echo "  Éditez .env et ajoutez ANTHROPIC_API_KEY"
    echo ""
    exit 1
fi

# Vérifie si l'environnement virtuel existe
if [ ! -d ../.venv ]; then
    echo "[ERREUR] Environnement virtuel manquant !"
    echo ""
    echo "Installez d'abord : python -m venv ../.venv"
    echo ""
    exit 1
fi

echo "[INFO] Activation de l'environnement virtuel..."
source ../.venv/bin/activate

echo "[INFO] Lancement de Streamlit..."
echo ""
echo "Le chatbot va s'ouvrir dans votre navigateur."
echo "Pour partager avec votre équipe, utilisez l'adresse réseau affichée."
echo ""
echo "Appuyez sur Ctrl+C pour arrêter le serveur."
echo ""

streamlit run app.py
