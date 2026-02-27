# 🐳 Docker Quick Start (5 minutes)

Guide ultra-rapide pour démarrer le chatbot avec Docker.

## Étape 1 : Vérifier les prérequis (30 sec)

```bash
# Vérifier Docker
docker --version

# Vérifier Docker Compose
docker-compose --version
```

Si pas installé : https://docs.docker.com/get-docker/

## Étape 2 : Ajouter la clé API Claude (1 min)

Éditez `.env` et ajoutez votre clé :

```env
ANTHROPIC_API_KEY=sk-ant-api03-VOTRE_CLE_ICI
```

Les autres variables (DSS_URL, DSS_API_KEY) sont déjà configurées ✅

## Étape 3 : Lancer (2 min)

```bash
# Option 1 : Avec Make (recommandé)
make up

# Option 2 : Avec Docker Compose
docker-compose up -d
```

## Étape 4 : Accéder (10 sec)

Ouvrez votre navigateur : **http://localhost:8501**

🎉 **C'est tout !** Le chatbot est prêt.

## 📊 Vérifications

```bash
# Voir les logs
make logs
# ou
docker-compose logs -f

# Vérifier le statut
make status
# ou
docker-compose ps
```

## 🛑 Arrêter

```bash
make down
# ou
docker-compose down
```

## 🔧 Commandes utiles

```bash
make help          # Toutes les commandes
make restart       # Redémarrer
make shell         # Shell dans le conteneur
make clean         # Tout nettoyer
```

## 🐛 Problèmes ?

**Port 8501 déjà utilisé** :
```bash
# Changer le port dans docker-compose.yml
ports:
  - "8502:8501"
```

**Variables d'env non chargées** :
```bash
docker-compose down
docker-compose up -d
```

**Erreur de build** :
```bash
make clean-all
make build
make up
```

---

**Pour en savoir plus** : Voir `DOCKER.md`
