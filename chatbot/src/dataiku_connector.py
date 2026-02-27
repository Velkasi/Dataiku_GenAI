"""
dataiku_connector.py - Connexion et interactions avec Dataiku DSS

Réutilise le code API existant du projet parent.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

# Ajoute le répertoire parent au PYTHONPATH pour importer src.api
parent_dir = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(parent_dir))

from src.api import (
    get_client,
    get_project,
    list_projects,
    list_datasets,
    get_dataset_as_dataframe,
    get_project_summary
)
from src.api.datasets import get_dataset_schema


class DataikuConnector:
    """Connecteur pour interagir avec Dataiku DSS"""

    def __init__(self, project_key: Optional[str] = None):
        """
        Initialise le connecteur Dataiku.

        Args:
            project_key: Clé du projet (utilise .env si None)
        """
        self.project_key = project_key or os.getenv("DSS_PROJECT_KEY")
        self.client = get_client()
        self.project = get_project(self.project_key)

    def get_available_datasets(self) -> List[str]:
        """
        Liste tous les datasets disponibles dans le projet.

        Returns:
            Liste des noms de datasets
        """
        return list_datasets(self.project_key)

    def get_dataset_info(self, dataset_name: str) -> Dict[str, Any]:
        """
        Récupère les informations d'un dataset (schéma, colonnes, etc.).

        Args:
            dataset_name: Nom du dataset

        Returns:
            Dict avec schema, columns, types
        """
        schema = get_dataset_schema(dataset_name, self.project_key)

        columns_info = []
        for col in schema.get("columns", []):
            columns_info.append({
                "name": col["name"],
                "type": col["type"],
                "meaning": col.get("meaning", "")
            })

        return {
            "name": dataset_name,
            "columns": columns_info,
            "nb_columns": len(columns_info)
        }

    def get_all_datasets_info(self) -> str:
        """
        Récupère les informations de tous les datasets disponibles.

        Returns:
            Texte formaté avec les infos des datasets
        """
        datasets = self.get_available_datasets()

        if not datasets:
            return "Aucun dataset disponible dans ce projet."

        info_lines = [f"📊 {len(datasets)} dataset(s) disponible(s) :\n"]

        for ds_name in datasets:
            try:
                ds_info = self.get_dataset_info(ds_name)
                columns_str = ", ".join([f"{c['name']} ({c['type']})"
                                        for c in ds_info['columns'][:5]])
                if len(ds_info['columns']) > 5:
                    columns_str += f", ... ({ds_info['nb_columns']} total)"

                info_lines.append(
                    f"  • {ds_name}\n"
                    f"    Colonnes : {columns_str}"
                )
            except Exception as e:
                info_lines.append(f"  • {ds_name} (erreur : {e})")

        return "\n".join(info_lines)

    def get_project_summary(self) -> Dict[str, Any]:
        """
        Résumé du projet (datasets, recettes, scénarios).

        Returns:
            Dict avec project_key, datasets, recipes, scenarios
        """
        return get_project_summary(self.project_key)

    def create_dataset(self, dataset_name: str, dataset_type: str = "managed") -> Any:
        """
        Crée un nouveau dataset dans le projet.

        Args:
            dataset_name: Nom du dataset
            dataset_type: Type de dataset (managed, sql, etc.)

        Returns:
            Dataset créé
        """
        # Utilise l'API Dataiku pour créer un dataset
        if dataset_type == "managed":
            dataset = self.project.create_dataset(
                dataset_name,
                type="Filesystem",
                params={"connection": "filesystem_managed", "path": f"/{dataset_name}"}
            )
        else:
            raise ValueError(f"Type de dataset non supporté : {dataset_type}")

        return dataset

    def dataset_exists(self, dataset_name: str) -> bool:
        """
        Vérifie si un dataset existe.

        Args:
            dataset_name: Nom du dataset

        Returns:
            True si le dataset existe
        """
        try:
            self.project.get_dataset(dataset_name)
            return True
        except:
            return False


def get_connector(project_key: Optional[str] = None) -> DataikuConnector:
    """
    Factory function pour créer un connecteur Dataiku.

    Args:
        project_key: Clé du projet

    Returns:
        Instance de DataikuConnector
    """
    return DataikuConnector(project_key)
