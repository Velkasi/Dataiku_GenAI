"""
demo.py - Script de démonstration complet

Exécutez ce script pour valider votre connexion Dataiku DSS et
explorer les fonctionnalités disponibles.

Usage :
    python scripts/demo.py
"""

import sys
from pathlib import Path

# Ajoute la racine du projet au PYTHONPATH pour les imports src.*
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.utils.logger import setup_logging
from src.api import (
    get_client,
    list_projects,
    get_project_summary,
    get_dataset_as_dataframe,
)

logger = setup_logging("demo")


def demo_connexion() -> bool:
    """Étape 1 : Test de connexion."""
    print("\n" + "=" * 60)
    print("  ÉTAPE 1 — Test de connexion à Dataiku DSS")
    print("=" * 60)

    try:
        client = get_client()
        info = client.get_auth_info()
        print(f"  Connecté en tant que : {info.get('authIdentifier', 'inconnu')}")
        print(f"  Type d'auth          : {info.get('authSource', 'inconnu')}")
        print("  Statut               : OK")
        return True
    except Exception as exc:
        print(f"  ERREUR de connexion : {exc}")
        print("  Vérifiez votre .env (DSS_URL, DSS_API_KEY).")
        return False


def demo_list_projects() -> list:
    """Étape 2 : Liste des projets."""
    print("\n" + "=" * 60)
    print("  ÉTAPE 2 — Liste des projets accessibles")
    print("=" * 60)

    projects = list_projects()
    if not projects:
        print("  Aucun projet accessible avec cette clé API.")
        return []

    print(f"  {len(projects)} projet(s) trouvé(s) :\n")
    for p in projects:
        print(f"    [{p['projectKey']}] {p['name']}")

    return projects


def demo_project_details(project_key: str) -> None:
    """Étape 3 : Détails d'un projet spécifique."""
    print("\n" + "=" * 60)
    print(f"  ÉTAPE 3 — Détails du projet '{project_key}'")
    print("=" * 60)

    try:
        summary = get_project_summary(project_key)
        print(f"  Datasets  : {', '.join(summary['datasets']) or 'aucun'}")
        print(f"  Recettes  : {', '.join(summary['recipes']) or 'aucune'}")
        print(f"  Scénarios : {', '.join(summary['scenarios']) or 'aucun'}")
    except Exception as exc:
        print(f"  ERREUR : {exc}")


def demo_dataset(project_key: str, dataset_name: str) -> None:
    """Étape 4 : Récupération d'un dataset."""
    print("\n" + "=" * 60)
    print(f"  ÉTAPE 4 — Lecture du dataset '{dataset_name}'")
    print("=" * 60)

    try:
        df = get_dataset_as_dataframe(dataset_name, project_key=project_key, limit=5)
        print(f"  Dimensions : {df.shape[0]} lignes × {df.shape[1]} colonnes")
        print(f"  Colonnes   : {', '.join(df.columns.tolist())}")
        print("\n  Aperçu (5 premières lignes) :")
        print(df.to_string(index=False))
    except Exception as exc:
        print(f"  ERREUR lecture dataset : {exc}")


if __name__ == "__main__":
    print("\n  Dataiku DSS x VS Code — Script de démonstration")

    # Étape 1 : connexion
    if not demo_connexion():
        sys.exit(1)

    # Étape 2 : liste des projets
    projects = demo_list_projects()

    if projects:
        # Utilise le premier projet trouvé (ou DSS_PROJECT_KEY du .env)
        import os
        from dotenv import load_dotenv
        load_dotenv()
        project_key = os.getenv("DSS_PROJECT_KEY") or projects[0]["projectKey"]

        # Étape 3 : détails du projet
        demo_project_details(project_key)

        # Étape 4 : dataset — changez "mon_dataset" par un vrai nom
        dataset_name = os.getenv("DEMO_DATASET", "mon_dataset")
        if dataset_name != "mon_dataset":
            demo_dataset(project_key, dataset_name)
        else:
            print(
                "\n  INFO : Ajoutez DEMO_DATASET=nom_du_dataset dans .env "
                "pour tester la lecture d'un dataset réel."
            )

    print("\n  Démonstration terminée.\n")
