# Dataiku DSS × VS Code — Guide de connexion

Connexion sécurisée entre Visual Studio Code et un serveur Dataiku DSS,
avec gestion des credentials via `.env`, scripts Python prêts à l'emploi
et intégration GitHub Copilot.

---

## Structure du projet

```
Dataiku_GenAI/
├── .env.example          ← Modèle de configuration (à copier en .env)
├── .gitignore            ← Exclusions Git (inclut .env)
├── requirements.txt      ← Dépendances Python
├── pyproject.toml        ← Config Ruff + pytest
│
├── src/
│   ├── api/
│   │   ├── client.py     ← Connexion sécurisée à DSS
│   │   ├── projects.py   ← Lister et inspecter les projets
│   │   └── datasets.py   ← Lire / écrire des datasets
│   ├── recipes/
│   │   └── generator.py  ← Génération de recettes (+ intégration Copilot)
│   └── utils/
│       └── logger.py     ← Logging configurable via .env
│
├── scripts/
│   ├── demo.py           ← Démonstration complète (connexion → dataset)
│   └── rotate_api_key.py ← Rotation sécurisée de la clé API
│
├── notebooks/
│   └── exploration.py    ← Exploration interactive (Jupyter-style)
│
├── tests/
│   └── test_connection.py ← Tests unitaires (mocks, pas de connexion réelle)
│
└── .vscode/
    ├── settings.json     ← Paramètres VS Code (Python, Copilot, Ruff)
    ├── extensions.json   ← Extensions recommandées
    ├── launch.json       ← Configurations de débogage
    └── dataiku.http      ← Tests REST direct de l'API DSS
```

---

## Installation rapide

### 1. Cloner et créer l'environnement virtuel

```bash
git clone <url-du-repo>
cd Dataiku_GenAI

python -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Configurer les credentials

```bash
cp .env.example .env
```

Éditez `.env` :

```env
DSS_URL=https://dss.mondomaine.local
DSS_API_KEY=votre_api_key_personnelle
DSS_PROJECT_KEY=MON_PROJET
```

> **Où trouver votre clé API ?**
> DSS → Profil utilisateur → Paramètres → Clés API personnelles → Créer une clé

### 3. Tester la connexion

```bash
python scripts/demo.py
```

### 4. Lancer les tests

```bash
pytest tests/ -v
```

---

## Extensions VS Code recommandées

VS Code proposera automatiquement l'installation des extensions listées
dans `.vscode/extensions.json`. Acceptez l'invitation ou installez via :

```
Ctrl+Shift+X → "@recommended"
```

Extensions clés :
| Extension | Rôle |
|---|---|
| `ms-python.python` | Support Python de base |
| `charliermarsh.ruff` | Linting + formatting ultra-rapide |
| `github.copilot` | Autocomplétion IA |
| `github.copilot-chat` | Chat IA contextuel |
| `ms-toolsai.jupyter` | Notebooks interactifs |
| `humao.rest-client` | Tester l'API DSS directement |

---

## Intégration GitHub Copilot

### Autocomplétion de recettes

Ouvrez `src/recipes/generator.py` ou `notebooks/exploration.py`,
puis écrivez un commentaire décrivant la transformation souhaitée :

```python
# Filtre les clients avec un score > 80 et calcule la moyenne par région
```

Appuyez sur **Tab** pour accepter la suggestion Copilot.

### Copilot Chat (Ctrl+I)

Sélectionnez du code et demandez :
- `"Explique cette fonction"`
- `"Génère une recette Dataiku pour joindre ces deux datasets"`
- `"Ajoute la gestion d'erreurs"`

Le contexte Dataiku est injecté automatiquement via `settings.json`.

---

## Sécurité

| Pratique | Implémentation |
|---|---|
| Pas de secrets dans le code | Variables d'environnement via `.env` |
| `.env` exclu de Git | `.gitignore` configuré |
| SSL activé par défaut | `DSS_SSL_VERIFY=true` (désactivable seulement en dev) |
| Rotation de clé API | `scripts/rotate_api_key.py` |
| Validation des variables | `DataikuConfig._require()` lève une erreur claire |

### Rotation de la clé API (recommandé tous les 90 jours)

```bash
python scripts/rotate_api_key.py
```

### Audit des accès

Consultez régulièrement dans DSS :
`Administration → Sécurité → Journal d'audit`

---

## Utilisation programmatique

```python
from src.api import get_client, list_projects, get_dataset_as_dataframe

# Connexion
client = get_client()

# Lister les projets
projects = list_projects()

# Lire un dataset
df = get_dataset_as_dataframe("nom_dataset", project_key="MON_PROJET", limit=1000)
print(df.head())
```

---

## Débogage dans VS Code

Utilisez les configurations du fichier `.vscode/launch.json` :

- **Demo - Connexion Dataiku** : exécute `scripts/demo.py` avec le débogueur
- **Script courant** : débogue le fichier Python actif (F5)
- **Tests pytest** : exécute tous les tests avec le débogueur
