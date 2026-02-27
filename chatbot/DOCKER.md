# 🐳 Docker Deployment Guide

Guide de déploiement Docker et Docker Compose pour le chatbot Dataiku.

## 🚀 Quick Start avec Docker Compose

### 1. Configuration

Assurez-vous que le fichier `.env` contient vos credentials :

```bash
# Vérifiez .env
cat .env

# Doit contenir :
ANTHROPIC_API_KEY=sk-ant-api03-...
DSS_URL=https://...
DSS_API_KEY=...
DSS_PROJECT_KEY=TEST_WORKFLOW
```

### 2. Build et lancement

```bash
# Avec Make (recommandé)
make up

# Ou avec docker-compose directement
docker-compose up -d
```

### 3. Accès

Ouvrez votre navigateur : **http://localhost:8501**

## 🎯 Commandes Make

Le `Makefile` simplifie toutes les opérations :

```bash
make help          # Affiche toutes les commandes disponibles
make check-env     # Vérifie la configuration
make build         # Build l'image Docker
make up            # Démarre le chatbot
make down          # Arrête le chatbot
make restart       # Redémarre
make logs          # Affiche les logs
make logs-f        # Suit les logs en temps réel
make shell         # Shell dans le conteneur
make status        # Statut du conteneur
make clean         # Nettoie tout
```

## 🔧 Commandes Docker Compose

### Build et démarrage

```bash
# Build l'image
docker-compose build

# Démarre en arrière-plan
docker-compose up -d

# Démarre avec logs
docker-compose up

# Build et démarre
docker-compose up -d --build
```

### Gestion

```bash
# Arrêter
docker-compose down

# Redémarrer
docker-compose restart

# Voir les logs
docker-compose logs -f

# Statut
docker-compose ps
```

### Debug

```bash
# Shell dans le conteneur
docker-compose exec dataiku-chatbot /bin/bash

# Logs en temps réel
docker-compose logs -f dataiku-chatbot

# Inspecter le conteneur
docker inspect dataiku-workflow-chatbot
```

## 📦 Build Docker manuel

Si vous préférez ne pas utiliser docker-compose :

```bash
# Build l'image
docker build -t dataiku-chatbot:latest .

# Run le conteneur
docker run -d \
  --name dataiku-workflow-chatbot \
  --env-file .env \
  -p 8501:8501 \
  --restart unless-stopped \
  dataiku-chatbot:latest

# Logs
docker logs -f dataiku-workflow-chatbot

# Stop
docker stop dataiku-workflow-chatbot

# Remove
docker rm dataiku-workflow-chatbot
```

## 🌐 Déploiement sur serveur

### Sur une VM ou serveur distant

1. **Copier les fichiers** :
```bash
scp -r chatbot/ user@server:/path/to/deployment/
```

2. **Sur le serveur** :
```bash
cd /path/to/deployment/chatbot
docker-compose up -d
```

3. **Accès depuis le réseau** :
Le service est accessible sur `http://server-ip:8501`

### Avec exposition externe

Modifiez `docker-compose.yml` pour binder sur toutes les interfaces :

```yaml
ports:
  - "0.0.0.0:8501:8501"  # Accessible depuis l'extérieur
```

**⚠️ Sécurité** : Ajoutez un reverse proxy (nginx) avec HTTPS en production !

## 🔒 Variables d'environnement

Le conteneur supporte ces variables (définies dans `.env`) :

```env
# Claude API (obligatoire)
ANTHROPIC_API_KEY=sk-ant-api03-...

# Dataiku DSS (obligatoires)
DSS_URL=https://dss.example.com
DSS_API_KEY=dkuaps-...
DSS_PROJECT_KEY=PROJET

# Optionnelles
DSS_SSL_VERIFY=true
DSS_TIMEOUT=30

# Streamlit (déjà configurées)
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
```

## 📊 Monitoring

### Healthcheck

Le conteneur a un healthcheck intégré :

```bash
# Vérifier la santé
docker inspect dataiku-workflow-chatbot | grep -A 5 Health

# Ou via Make
make health
```

### Logs

```bash
# Logs avec timestamps
docker-compose logs -f --timestamps

# Dernières 100 lignes
docker-compose logs --tail=100

# Logs d'un service spécifique
docker-compose logs dataiku-chatbot
```

### Ressources

```bash
# Utilisation CPU/RAM
docker stats dataiku-workflow-chatbot

# Avec Make
make status
```

## 🧹 Nettoyage

```bash
# Arrêter et supprimer le conteneur
make down

# Supprimer conteneur + volumes
make clean

# Supprimer tout (conteneur + volumes + images)
make clean-all
```

## 🐛 Troubleshooting

### Le conteneur ne démarre pas

```bash
# Vérifier les logs
docker-compose logs

# Vérifier la config
make check-env

# Rebuild from scratch
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### Port 8501 déjà utilisé

```bash
# Trouver le processus
netstat -ano | findstr :8501  # Windows
lsof -i :8501                 # Linux/Mac

# Changer le port dans docker-compose.yml
ports:
  - "8502:8501"  # Utilise 8502 sur l'hôte
```

### Variables d'environnement non chargées

```bash
# Vérifier que .env existe
ls -la .env

# Rebuild avec nouvelle config
docker-compose down
docker-compose up -d
```

### Permission denied (Linux)

```bash
# Ajouter votre user au groupe docker
sudo usermod -aG docker $USER

# Logout/login puis tester
docker ps
```

## 📋 Checklist de production

Avant de déployer en production :

- [ ] `.env` configuré avec vraies credentials
- [ ] SSL/TLS activé (DSS_SSL_VERIFY=true)
- [ ] Reverse proxy (nginx/traefik) configuré
- [ ] HTTPS activé avec certificat valide
- [ ] Firewall configuré (port 8501 filtré)
- [ ] Monitoring en place (logs, healthchecks)
- [ ] Backup des données (si persistence activée)
- [ ] Limites de ressources ajustées
- [ ] Image taguée avec version (pas latest)

## 🚀 Migration vers Kubernetes

Une fois le Docker Compose fonctionnel, voir `HELM.md` pour déployer sur Kubernetes.

---

**Créé avec ❤️ par Claude Code**
