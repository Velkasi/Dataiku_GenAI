"""
projects.py - Opérations sur les projets Dataiku DSS

Fournit des fonctions pour lister, inspecter et interagir
avec les projets disponibles sur le serveur DSS.
"""

import logging
from typing import List, Dict, Any

from .client import get_client, get_project

logger = logging.getLogger(__name__)


def list_projects() -> List[Dict[str, Any]]:
    """
    Liste tous les projets accessibles avec la clé API courante.

    Returns:
        Liste de dicts contenant les métadonnées de chaque projet.

    Example:
        >>> projects = list_projects()
        >>> for p in projects:
        ...     print(p["projectKey"], "-", p["name"])
    """
    client = get_client()
    projects = client.list_projects()
    logger.info("%d projet(s) trouvé(s).", len(projects))
    return projects


def get_project_summary(project_key: str) -> Dict[str, Any]:
    """
    Retourne un résumé structuré d'un projet : datasets, recettes, jobs.

    Args:
        project_key: Clé du projet (ex: 'MON_PROJET').

    Returns:
        Dict avec les clés 'datasets', 'recipes', 'scenarios'.
    """
    project = get_project(project_key)

    datasets = [ds.name for ds in project.list_datasets()]
    recipes = [r.metadata["name"] for r in project.list_recipes()]
    scenarios = [s["id"] for s in project.list_scenarios()]

    summary = {
        "project_key": project_key,
        "datasets": datasets,
        "recipes": recipes,
        "scenarios": scenarios,
    }

    logger.info(
        "Projet '%s' : %d dataset(s), %d recette(s), %d scénario(s).",
        project_key, len(datasets), len(recipes), len(scenarios),
    )
    return summary


def list_datasets(project_key: str) -> List[str]:
    """
    Liste les noms de tous les datasets d'un projet.

    Args:
        project_key: Clé du projet.

    Returns:
        Liste des noms de datasets.
    """
    project = get_project(project_key)
    return [ds.name for ds in project.list_datasets()]
