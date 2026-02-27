# 📦 Résumé du déploiement - Dataiku Chatbot

Guide rapide pour choisir et déployer le chatbot selon votre environnement.

## 🎯 Options de déploiement disponibles

| Option | Environnement | Complexité | Temps setup | Scalabilité |
|--------|---------------|------------|-------------|-------------|
| **Local (Python)** | Dev/Test | ⭐ Simple | 5 min | ❌ |
| **Docker Compose** | MVP/Production | ⭐⭐ Facile | 5 min | ⭐ Limited |
| **Kubernetes + Helm** | Production | ⭐⭐⭐ Avancé | 30 min | ⭐⭐⭐ Full |

## 🚀 Déploiement recommandé par cas d'usage

### 🧪 Cas 1 : Test / Développement local
**Utiliser : Installation locale Python**

```bash
cd chatbot
../.venv/Scripts/activate
streamlit run app.py
```

📖 **Guide** : `QUICKSTART.md`

---

### 🏢 Cas 2 : MVP en entreprise (serveur unique)
**Utiliser : Docker Compose** ✅ **RECOMMANDÉ**

```bash
# 1. Config
echo "ANTHROPIC_API_KEY=sk-ant-api03-..." >> .env

# 2. Launch
make up
```

📖 **Guides** :
- `DOCKER-QUICKSTART.md` (5 min)
- `DOCKER.md` (complet)

**Avantages** :
- ✅ Isolation complète
- ✅ Reproductible
- ✅ Pas de dépendances système
- ✅ Accessible par toute l'équipe
- ✅ Prêt pour prod

---

### ☸️ Cas 3 : Production scalable (cluster K8s)
**Utiliser : Kubernetes + Helm**

```bash
# 1. Build & Push image
docker build -t registry.company.com/dataiku-chatbot:v1.0.0 .
docker push registry.company.com/dataiku-chatbot:v1.0.0

# 2. Create secret
kubectl create secret generic dataiku-chatbot-secrets \
  --from-literal=ANTHROPIC_API_KEY='sk-ant-...' \
  --from-literal=DSS_URL='...' \
  --from-literal=DSS_API_KEY='...'

# 3. Deploy
helm install dataiku-chatbot ./helm/dataiku-chatbot \
  --set image.repository=registry.company.com/dataiku-chatbot \
  --set image.tag=v1.0.0
```

📖 **Guide** : `HELM.md`

**Avantages** :
- ✅ Autoscaling (HPA)
- ✅ Rolling updates
- ✅ High availability
- ✅ Load balancing
- ✅ Monitoring intégré

---

## 📁 Structure complète du projet

```
chatbot/
├── 🐍 Python App
│   ├── app.py                      # Interface Streamlit
│   ├── src/
│   │   ├── chat_handler.py         # Claude API
│   │   ├── dataiku_connector.py    # Dataiku API
│   │   ├── workflow_builder.py     # Création workflows
│   │   └── prompts.py              # Prompts système
│   └── requirements.txt
│
├── 🐳 Docker
│   ├── Dockerfile                  # Image multi-stage optimisée
│   ├── docker-compose.yml          # Orchestration
│   ├── .dockerignore
│   └── Makefile                    # Commandes simplifiées
│
├── ☸️ Kubernetes (Helm)
│   └── helm/dataiku-chatbot/
│       ├── Chart.yaml              # Metadata
│       ├── values.yaml             # Configuration
│       └── templates/
│           ├── deployment.yaml
│           ├── service.yaml
│           ├── ingress.yaml
│           └── serviceaccount.yaml
│
└── 📚 Documentation
    ├── README.md                   # Doc principale
    ├── QUICKSTART.md               # Guide 5min (local)
    ├── DOCKER-QUICKSTART.md        # Guide 5min (Docker)
    ├── DOCKER.md                   # Guide complet Docker
    ├── HELM.md                     # Guide complet K8s
    ├── DEPLOYMENT-SUMMARY.md       # Ce fichier
    ├── start.bat / start.sh        # Scripts lancement local
```

## 🔑 Configuration requise

### Toutes les options nécessitent :

```env
# Claude API
ANTHROPIC_API_KEY=sk-ant-api03-...

# Dataiku DSS
DSS_URL=https://dss.example.com
DSS_API_KEY=dkuaps-...
DSS_PROJECT_KEY=TEST_WORKFLOW
DSS_SSL_VERIFY=true
```

### Localisation du .env :

| Déploiement | Localisation |
|-------------|--------------|
| Local Python | `chatbot/.env` |
| Docker Compose | `chatbot/.env` (monté comme volume) |
| Kubernetes | Secret K8s : `dataiku-chatbot-secrets` |

## 🎯 Workflow de migration

### Phase 1 : MVP (Semaine 1)
```
Développement local → Docker Compose sur serveur unique
```

### Phase 2 : Pre-production (Semaine 2-3)
```
Docker Compose → Helm Chart → Deploy sur K8s staging
```

### Phase 3 : Production (Semaine 4)
```
K8s staging validé → Deploy sur K8s production avec monitoring
```

## 🛠️ Commandes par environnement

### Local (Python)
```bash
cd chatbot
../.venv/Scripts/activate    # Windows
source ../.venv/bin/activate # Linux/Mac
streamlit run app.py
```

### Docker Compose
```bash
make help          # Toutes les commandes
make up            # Démarrer
make logs          # Voir les logs
make down          # Arrêter
make clean         # Nettoyer
```

### Kubernetes
```bash
# Deploy
helm install dataiku-chatbot ./helm/dataiku-chatbot

# Upgrade
helm upgrade dataiku-chatbot ./helm/dataiku-chatbot

# Status
kubectl get pods -l app.kubernetes.io/name=dataiku-chatbot

# Logs
kubectl logs -f -l app.kubernetes.io/name=dataiku-chatbot

# Uninstall
helm uninstall dataiku-chatbot
```

## 📊 Monitoring

### Docker Compose
```bash
# Healthcheck
make health

# Resources
docker stats dataiku-workflow-chatbot

# Logs
make logs-f
```

### Kubernetes
```bash
# Pods status
kubectl get pods

# Resources
kubectl top pods

# HPA status
kubectl get hpa

# Logs
kubectl logs -f <pod-name>
```

## 🔒 Sécurité par environnement

### Local
- ⚠️ .env non commité (.gitignore)
- ⚠️ Accessible uniquement sur localhost

### Docker
- ✅ User non-root dans conteneur
- ✅ Secrets via .env (à protéger)
- ✅ Healthchecks intégrés
- ⚠️ Ajouter reverse proxy pour HTTPS

### Kubernetes
- ✅ Secrets K8s (encrypted at rest)
- ✅ RBAC + ServiceAccount
- ✅ Network Policies
- ✅ Pod Security Standards
- ✅ HTTPS via Ingress + cert-manager

## 🚨 Troubleshooting rapide

### ❌ Erreur "ANTHROPIC_API_KEY non définie"
```bash
# Vérifier .env (Docker/Local)
cat .env | grep ANTHROPIC

# Vérifier secret (K8s)
kubectl get secret dataiku-chatbot-secrets -o yaml
```

### ❌ Port 8501 déjà utilisé
```bash
# Changer le port dans docker-compose.yml
ports:
  - "8502:8501"
```

### ❌ Image pull error (K8s)
```bash
# Vérifier imagePullSecret
kubectl get secret regcred

# Recréer si besoin
kubectl create secret docker-registry regcred ...
```

### ❌ Pod crashe (K8s)
```bash
# Logs du container qui crash
kubectl logs <pod-name> --previous

# Events
kubectl describe pod <pod-name>
```

## 📞 Support

- **Documentation locale** : Voir README.md, DOCKER.md, HELM.md
- **Logs** : Toujours commencer par vérifier les logs
- **Issues** : Créer une issue sur le repo Git

## ✅ Checklist de production

Avant de déployer en production :

### Docker Compose
- [ ] .env avec vraies credentials
- [ ] SSL/TLS activé
- [ ] Reverse proxy configuré (nginx/traefik)
- [ ] Firewall configuré
- [ ] Logs monitoring
- [ ] Backup strategy

### Kubernetes
- [ ] Image dans registry privé
- [ ] Secrets K8s créés
- [ ] Ingress + HTTPS configuré
- [ ] Resources limits/requests définis
- [ ] HPA activé
- [ ] Monitoring (Prometheus/Grafana)
- [ ] Alerting configuré
- [ ] Network policies en place
- [ ] Backup + Disaster recovery plan

---

## 🎉 Prêt à déployer !

Choisissez votre option et suivez le guide correspondant :

- 🧪 **Test** → `QUICKSTART.md`
- 🐳 **MVP** → `DOCKER-QUICKSTART.md`
- ☸️ **Production** → `HELM.md`

**Bon déploiement ! 🚀**
