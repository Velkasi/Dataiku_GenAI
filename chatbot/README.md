# 🤖 Dataiku Workflow Creator Chatbot

Chatbot conversationnel basé sur Claude AI pour créer des workflows Dataiku automatiquement via une interface Streamlit.

## 🎯 Fonctionnalités

- **Chat conversationnel** avec Claude AI
- **Analyse automatique** des datasets disponibles
- **Création de workflows** complets (datasets + recettes)
- **Support multi-recettes** : Python, Grouping, Join
- **Interface web moderne** accessible par toute l'équipe
- **Zéro configuration** : réutilise la config Dataiku existante
- **Déploiement Docker** : MVP prêt pour production
- **Helm Chart K8s** : Scalable sur Kubernetes

## 🚀 Installation rapide

### Option 1 : Docker (recommandé pour MVP/Production)

**Le moyen le plus rapide et fiable** :

```bash
# 1. Ajoutez votre clé API Claude dans .env
echo "ANTHROPIC_API_KEY=sk-ant-api03-..." >> .env

# 2. Lancez avec Make
make up

# 3. Ou avec Docker Compose
docker-compose up -d
```

🌐 **Accès** : http://localhost:8501

📚 **Documentation complète** :
- `DOCKER-QUICKSTART.md` - Guide 5 minutes
- `DOCKER.md` - Guide complet Docker
- `HELM.md` - Déploiement Kubernetes

### Option 2 : Installation locale (développement)

### 1. Configuration de l'API Claude

Obtenez une clé API Claude sur : https://console.anthropic.com/

### 2. Installation des dépendances

```bash
cd chatbot
pip install -r requirements.txt
```

### 3. Configuration (.env)

Créez un fichier `.env` :

```bash
cp .env.example .env
```

Éditez `.env` et ajoutez votre clé API Claude :

```env
ANTHROPIC_API_KEY=sk-ant-api03-...

# Les autres variables sont héritées du projet parent
DSS_URL=https://dss-ed6dfc0f-8303e211-dku.eu-west-3.app.dataiku.io
DSS_API_KEY=dkuaps-...
DSS_PROJECT_KEY=TEST_WORKFLOW
DSS_SSL_VERIFY=true
```

### 4. Lancement

```bash
streamlit run app.py
```

Le chatbot s'ouvre dans votre navigateur : **http://localhost:8501**

## 📱 Accès par l'équipe (réseau local)

Pour que vos collègues accèdent au chatbot :

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

Ils peuvent alors accéder via : **http://votre-ip:8501**

## 💬 Exemples d'utilisation

### Exemple 1 : Agrégation simple

```
Vous: "Crée un workflow qui agrège healthcare_dataset par patient_id
      avec la somme des montants"

Bot: [Analyse le dataset]
     [Propose un workflow avec recette Grouping]
     [Demande confirmation]

Vous: "oui"

Bot: [Crée le workflow dans DSS]
     ✅ Workflow créé ! Lien: https://dss.../flow/
```

### Exemple 2 : Jointure de datasets

```
Vous: "Je veux joindre Original_data et Expanded_data sur patient_id"

Bot: [Analyse les deux datasets]
     [Propose une recette Join]
     [Demande confirmation]

Vous: "oui"

Bot: [Crée le workflow]
     ✅ Recette join_data créée
```

### Exemple 3 : Nettoyage de données

```
Vous: "Nettoie healthcare_dataset en supprimant les lignes avec des nulls
      et garde seulement les patients avec age > 18"

Bot: [Propose une recette Python]
     [Montre le code généré]
     [Demande confirmation]

Vous: "oui"

Bot: [Crée la recette Python dans DSS]
```

## 🎨 Interface

L'interface Streamlit comprend :

**Zone principale (chat)** :
- Conversation avec Claude AI
- Message d'accueil avec guide
- Historique des messages

**Sidebar** :
- Informations du projet
- Liste des datasets disponibles
- Statistiques de conversation
- Guide d'utilisation rapide
- Bouton "Nouvelle conversation"

## 🧠 Comment ça marche ?

1. **Vous décrivez** ce que vous voulez en langage naturel
2. **Claude analyse** les datasets disponibles via l'API Dataiku
3. **Claude propose** un plan de workflow détaillé
4. **Vous confirmez** (ou demandez des modifications)
5. **Le workflow est créé** automatiquement dans DSS

## ⚙️ Architecture

```
chatbot/
├── app.py                      # Interface Streamlit
├── src/
│   ├── chat_handler.py         # Gestion Claude API + Tools
│   ├── dataiku_connector.py    # Connexion DSS (réutilise ../src/api)
│   ├── workflow_builder.py     # Création de workflows
│   └── prompts.py              # Prompts système pour Claude
├── requirements.txt
└── .env                        # Configuration
```

## 🔧 Types de recettes supportées

| Type | Description | Cas d'usage |
|------|-------------|-------------|
| **Python** | Code Python libre | Transformations complexes, nettoyage |
| **Grouping** | Agrégations | Sommes, moyennes, count par groupe |
| **Join** | Jointures SQL | Combiner plusieurs datasets |

*Plus de types à venir : Prepare, SQL, Sync, etc.*

## 💡 Conseils d'utilisation

**Soyez précis** :
- ✅ "Agrège par région avec la somme des ventes et le count"
- ❌ "Fais une agrégation"

**Nommez les datasets** :
- ✅ "Utilise healthcare_dataset comme source"
- ❌ "Utilise les données"

**Demandez des explications** :
- "Pourquoi tu proposes cette recette ?"
- "Quelle est la différence entre Join et Python ?"

## 🐛 Dépannage

### Erreur "ANTHROPIC_API_KEY non définie"
→ Vérifiez que `.env` contient votre clé API

### Erreur "No module named 'dataikuapi'"
→ Installez les dépendances : `pip install -r requirements.txt`

### Erreur de connexion Dataiku
→ Vérifiez `DSS_URL` et `DSS_API_KEY` dans `.env`

### Le chatbot ne répond pas
→ Vérifiez les logs dans le terminal Streamlit

## 📊 Optimisation des coûts

Le chatbot est optimisé pour limiter les coûts Claude :

- **Cache des datasets** : Récupérés une seule fois au démarrage
- **Prompts optimisés** : Instructions claires et concises
- **Tools Claude** : Appels API uniquement quand nécessaire

**Coût typique** : ~2000-3000 tokens/workflow ≈ $0.01 avec Claude Sonnet

## 🔒 Sécurité

- Les clés API ne sont jamais commitées (`.gitignore`)
- Connexion SSL à Dataiku par défaut
- Logs d'activité disponibles
- Pas de stockage de données sensibles

## 🚀 Évolutions futures

- [ ] Support de plus de types de recettes (Prepare, SQL, Sync)
- [ ] Export/Import de templates de workflows
- [ ] Historique des workflows créés
- [ ] Multi-projets Dataiku
- [ ] Authentification utilisateurs
- [ ] Déploiement sur serveur d'équipe

## 📝 Licence

Usage interne - Projet d'automatisation Dataiku

---

**Créé avec ❤️ par Claude Code**
