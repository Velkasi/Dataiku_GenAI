@echo off
REM Script de lancement du chatbot Dataiku

echo.
echo ========================================
echo  Dataiku Workflow Creator Chatbot
echo ========================================
echo.

REM Vérifie si .env existe
if not exist .env (
    echo [ERREUR] Fichier .env manquant !
    echo.
    echo Creez un fichier .env avec votre cle API Claude :
    echo   cp .env.example .env
    echo   Editez .env et ajoutez ANTHROPIC_API_KEY
    echo.
    pause
    exit /b 1
)

REM Vérifie si l'environnement virtuel existe
if not exist ..\.venv (
    echo [ERREUR] Environnement virtuel manquant !
    echo.
    echo Installez d'abord : python -m venv ../.venv
    echo.
    pause
    exit /b 1
)

echo [INFO] Activation de l'environnement virtuel...
call ..\.venv\Scripts\activate

echo [INFO] Lancement de Streamlit...
echo.
echo Le chatbot va s'ouvrir dans votre navigateur.
echo Pour partager avec votre equipe, utilisez l'adresse reseau affichee.
echo.
echo Appuyez sur Ctrl+C pour arreter le serveur.
echo.

streamlit run app.py

pause
