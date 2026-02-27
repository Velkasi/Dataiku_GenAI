# Multi-stage Dockerfile pour Dataiku Workflow Chatbot
# Optimisé pour production avec image légère

# ============================================================
# Stage 1: Builder - Installation des dépendances
# ============================================================
FROM python:3.10-slim as builder

# Métadonnées
LABEL maintainer="Data Engineering Team"
LABEL description="Dataiku Workflow Creator Chatbot with Claude AI"

# Variables d'environnement pour Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Créer un environnement virtuel
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copier et installer les requirements
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# ============================================================
# Stage 2: Runtime - Image finale légère
# ============================================================
FROM python:3.10-slim

# Variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH" \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Copier l'environnement virtuel depuis le builder
COPY --from=builder /opt/venv /opt/venv

# Créer un utilisateur non-root pour la sécurité
RUN useradd -m -u 1000 streamlit && \
    mkdir -p /app && \
    chown -R streamlit:streamlit /app

# Définir le répertoire de travail
WORKDIR /app

# Copier le code de l'application
COPY --chown=streamlit:streamlit app.py /app/
COPY --chown=streamlit:streamlit src/ /app/src/

# Copier le code parent (src/api) nécessaire pour dataiku_connector
COPY --chown=streamlit:streamlit ../src /parent_src

# Créer le dossier .streamlit pour la config
RUN mkdir -p /app/.streamlit && \
    chown streamlit:streamlit /app/.streamlit

# Configuration Streamlit
RUN echo '[server]\n\
port = 8501\n\
address = "0.0.0.0"\n\
headless = true\n\
enableCORS = false\n\
enableXsrfProtection = true\n\
\n\
[browser]\n\
gatherUsageStats = false\n\
\n\
[theme]\n\
primaryColor = "#1f77b4"\n\
backgroundColor = "#ffffff"\n\
secondaryBackgroundColor = "#f0f2f6"\n\
textColor = "#262730"\n\
' > /app/.streamlit/config.toml

# Passer à l'utilisateur non-root
USER streamlit

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8501/_stcore/health', timeout=5)"

# Exposer le port Streamlit
EXPOSE 8501

# Point d'entrée
ENTRYPOINT ["streamlit", "run"]
CMD ["app.py"]
