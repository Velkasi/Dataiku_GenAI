"""
exploration.py - Notebook-style : exploration interactive d'un projet Dataiku

Utilisez ce script avec l'extension Jupyter de VS Code (# %%) ou
exécutez-le comme script standard.

GitHub Copilot tips :
  - Commencez une ligne par "# " et décrivez votre transformation
  - Appuyez sur Tab pour accepter la suggestion Copilot
  - Utilisez Ctrl+I (Copilot Chat) pour expliquer/refactorer du code
"""

# %% [markdown]
# ## Connexion et exploration Dataiku DSS

# %%
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.utils.logger import setup_logging
from src.api import get_client, list_projects, get_dataset_as_dataframe

setup_logging("notebook")

# %%
# Connexion et affichage des infos d'auth
client = get_client()
auth = client.get_auth_info()
print(f"Connecté : {auth.get('authIdentifier')}")

# %%
# Liste de tous les projets accessibles
projects = list_projects()
for p in projects:
    print(f"  {p['projectKey']:20s} {p['name']}")

# %%
# Lecture d'un dataset (remplacez les valeurs ci-dessous)
PROJECT_KEY = "MON_PROJET"   # <- votre clé projet
DATASET_NAME = "mon_dataset" # <- nom du dataset

df = get_dataset_as_dataframe(DATASET_NAME, project_key=PROJECT_KEY, limit=1000)
print(df.shape)
df.head()

# %%
# --- Copilot : décrivez votre analyse ci-dessous ---
# Exemple : "Calcule les statistiques descriptives par catégorie"


# %%
# --- Copilot : visualisation ---
# Exemple : "Affiche un histogramme de la colonne 'age'"
