"""
datasets.py - Lecture et écriture de datasets Dataiku DSS

Permet de récupérer des données depuis DSS sous forme de
pandas DataFrame, et d'y repousser des résultats.
"""

import logging
from typing import Optional

import pandas as pd

from .client import get_project

logger = logging.getLogger(__name__)


def get_dataset_as_dataframe(
    dataset_name: str,
    project_key: Optional[str] = None,
    limit: Optional[int] = None,
    infer_types: bool = True,
) -> pd.DataFrame:
    """
    Télécharge un dataset DSS et le retourne sous forme de DataFrame pandas.

    Args:
        dataset_name: Nom du dataset dans DSS.
        project_key: Clé du projet (utilise .env si None).
        limit: Nombre maximum de lignes à récupérer (None = tout).
        infer_types: Convertit automatiquement les types de colonnes.

    Returns:
        pd.DataFrame avec les données du dataset.

    Example:
        >>> df = get_dataset_as_dataframe("clients", limit=500)
        >>> print(df.head())
    """
    project = get_project(project_key)
    dataset = project.get_dataset(dataset_name)

    logger.info(
        "Récupération du dataset '%s'%s...",
        dataset_name,
        f" (limite : {limit} lignes)" if limit else "",
    )

    df = dataset.get_dataframe(limit=limit, infer_types=infer_types)
    logger.info("Dataset chargé : %d lignes × %d colonnes.", *df.shape)
    return df


def push_dataframe_to_dataset(
    df: pd.DataFrame,
    dataset_name: str,
    project_key: Optional[str] = None,
    overwrite: bool = True,
) -> None:
    """
    Pousse un DataFrame pandas vers un dataset DSS existant.

    Args:
        df: DataFrame à envoyer.
        dataset_name: Nom du dataset cible dans DSS.
        project_key: Clé du projet.
        overwrite: Si True, remplace les données existantes.

    Raises:
        ValueError: Si le DataFrame est vide.
    """
    if df.empty:
        raise ValueError("Le DataFrame est vide — aucune donnée à envoyer.")

    project = get_project(project_key)
    dataset = project.get_dataset(dataset_name)

    logger.info(
        "Envoi de %d lignes vers le dataset '%s'...",
        len(df), dataset_name,
    )

    with dataset.get_writer() as writer:
        if overwrite:
            writer.write_dataframe(df)
        else:
            writer.write_dataframe(df, write_initial_schema=False)

    logger.info("Dataset '%s' mis à jour avec succès.", dataset_name)


def get_dataset_schema(
    dataset_name: str,
    project_key: Optional[str] = None,
) -> dict:
    """
    Retourne le schéma (colonnes + types) d'un dataset.

    Args:
        dataset_name: Nom du dataset.
        project_key: Clé du projet.

    Returns:
        Dict avec la liste des colonnes et leurs types DSS.
    """
    project = get_project(project_key)
    dataset = project.get_dataset(dataset_name)
    schema = dataset.get_schema()
    logger.info(
        "Schéma de '%s' : %d colonne(s).",
        dataset_name, len(schema["columns"]),
    )
    return schema
