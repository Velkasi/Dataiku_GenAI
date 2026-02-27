"""
workflow_builder.py - Construction et création de workflows Dataiku

Gère la création de workflows complets (datasets + recettes) dans DSS.
"""

import logging
from typing import List, Dict, Any, Optional
from dataiku_connector import DataikuConnector

logger = logging.getLogger(__name__)


class WorkflowBuilder:
    """Construit et crée des workflows Dataiku"""

    def __init__(self, connector: DataikuConnector):
        """
        Initialise le builder.

        Args:
            connector: Instance de DataikuConnector
        """
        self.connector = connector
        self.project = connector.project

    def create_python_recipe(
        self,
        recipe_name: str,
        input_datasets: List[str],
        output_dataset: str,
        code: Optional[str] = None
    ) -> Any:
        """
        Crée une recette Python.

        Args:
            recipe_name: Nom de la recette
            input_datasets: Liste des datasets d'entrée
            output_dataset: Dataset de sortie
            code: Code Python (template si None)

        Returns:
            Recette créée
        """
        logger.info(f"Création recette Python : {recipe_name}")

        # Code par défaut si non fourni
        if code is None:
            code = self._generate_python_template(input_datasets, output_dataset)

        # Crée la recette via l'API
        builder = self.project.new_recipe("python", recipe_name)

        # Ajoute les inputs
        for ds in input_datasets:
            builder.with_input(ds)

        # Ajoute l'output
        builder.with_output(output_dataset)

        # Crée et configure
        recipe = builder.build()
        recipe.get_settings().set_code(code)
        recipe.get_settings().save()

        logger.info(f"Recette {recipe_name} créée avec succès")
        return recipe

    def create_grouping_recipe(
        self,
        recipe_name: str,
        input_dataset: str,
        output_dataset: str,
        group_by: List[str],
        aggregations: List[Dict[str, str]]
    ) -> Any:
        """
        Crée une recette Grouping (agrégation).

        Args:
            recipe_name: Nom de la recette
            input_dataset: Dataset d'entrée
            output_dataset: Dataset de sortie
            group_by: Colonnes pour grouper
            aggregations: Liste de {column, function, output}

        Returns:
            Recette créée
        """
        logger.info(f"Création recette Grouping : {recipe_name}")

        builder = self.project.new_recipe("grouping", recipe_name)
        builder.with_input(input_dataset)
        builder.with_output(output_dataset)

        recipe = builder.build()
        settings = recipe.get_settings()

        # Configuration du grouping
        payload = settings.get_recipe_raw_definition()
        payload["keys"] = [{"column": col} for col in group_by]
        payload["values"] = []

        for agg in aggregations:
            payload["values"].append({
                "column": agg["column"],
                "aggregation": agg["function"],
                "outputColumn": agg["output"]
            })

        settings.set_recipe_raw_definition(payload)
        settings.save()

        logger.info(f"Recette {recipe_name} créée avec succès")
        return recipe

    def create_join_recipe(
        self,
        recipe_name: str,
        left_dataset: str,
        right_dataset: str,
        output_dataset: str,
        join_keys: List[tuple],  # [(left_col, right_col), ...]
        join_type: str = "LEFT"
    ) -> Any:
        """
        Crée une recette Join.

        Args:
            recipe_name: Nom de la recette
            left_dataset: Dataset gauche
            right_dataset: Dataset droit
            output_dataset: Dataset de sortie
            join_keys: Paires de colonnes pour la jointure
            join_type: Type de join (LEFT, INNER, OUTER, etc.)

        Returns:
            Recette créée
        """
        logger.info(f"Création recette Join : {recipe_name}")

        builder = self.project.new_recipe("join", recipe_name)
        builder.with_input(left_dataset)
        builder.with_input(right_dataset)
        builder.with_output(output_dataset)

        recipe = builder.build()
        settings = recipe.get_settings()

        # Configuration du join
        payload = settings.get_recipe_raw_definition()
        payload["virtualInputs"] = [
            {"index": 0, "prefix": "left_"},
            {"index": 1, "prefix": "right_"}
        ]
        payload["joins"] = [{
            "table1": 0,
            "table2": 1,
            "type": join_type.upper(),
            "on": [{"column1": left, "column2": right} for left, right in join_keys]
        }]

        settings.set_recipe_raw_definition(payload)
        settings.save()

        logger.info(f"Recette {recipe_name} créée avec succès")
        return recipe

    def create_workflow(
        self,
        workflow_name: str,
        source_datasets: List[str],
        recipes: List[Dict[str, Any]],
        output_dataset: str
    ) -> Dict[str, Any]:
        """
        Crée un workflow complet.

        Args:
            workflow_name: Nom du workflow
            source_datasets: Datasets sources
            recipes: Liste des recettes à créer
            output_dataset: Dataset final

        Returns:
            Dict avec résumé de la création

        Example:
            recipes = [
                {
                    "type": "python",
                    "name": "clean_data",
                    "inputs": ["raw_data"],
                    "output": "cleaned_data",
                    "code": "# Python code..."
                },
                {
                    "type": "grouping",
                    "name": "aggregate",
                    "input": "cleaned_data",
                    "output": "aggregated_data",
                    "group_by": ["region"],
                    "aggregations": [
                        {"column": "amount", "function": "sum", "output": "total_amount"}
                    ]
                }
            ]
        """
        logger.info(f"Création workflow : {workflow_name}")

        created_recipes = []
        created_datasets = []

        try:
            # Crée le dataset de sortie final s'il n'existe pas
            if not self.connector.dataset_exists(output_dataset):
                self.connector.create_dataset(output_dataset)
                created_datasets.append(output_dataset)

            # Crée les recettes dans l'ordre
            for recipe_config in recipes:
                recipe_type = recipe_config["type"]
                recipe_name = recipe_config["name"]

                # Crée les datasets intermédiaires si nécessaire
                output = recipe_config.get("output", output_dataset)
                if not self.connector.dataset_exists(output) and output != output_dataset:
                    self.connector.create_dataset(output)
                    created_datasets.append(output)

                # Crée la recette selon son type
                if recipe_type == "python":
                    recipe = self.create_python_recipe(
                        recipe_name,
                        recipe_config["inputs"],
                        output,
                        recipe_config.get("code")
                    )
                elif recipe_type == "grouping":
                    recipe = self.create_grouping_recipe(
                        recipe_name,
                        recipe_config["input"],
                        output,
                        recipe_config["group_by"],
                        recipe_config["aggregations"]
                    )
                elif recipe_type == "join":
                    recipe = self.create_join_recipe(
                        recipe_name,
                        recipe_config["left"],
                        recipe_config["right"],
                        output,
                        recipe_config["join_keys"],
                        recipe_config.get("join_type", "LEFT")
                    )
                else:
                    raise ValueError(f"Type de recette non supporté : {recipe_type}")

                created_recipes.append(recipe_name)

            logger.info(f"Workflow {workflow_name} créé avec succès")

            return {
                "success": True,
                "workflow_name": workflow_name,
                "created_recipes": created_recipes,
                "created_datasets": created_datasets,
                "output_dataset": output_dataset
            }

        except Exception as e:
            logger.error(f"Erreur création workflow : {e}")
            return {
                "success": False,
                "error": str(e),
                "created_recipes": created_recipes,
                "created_datasets": created_datasets
            }

    def _generate_python_template(
        self,
        input_datasets: List[str],
        output_dataset: str
    ) -> str:
        """
        Génère un template Python par défaut.

        Args:
            input_datasets: Datasets d'entrée
            output_dataset: Dataset de sortie

        Returns:
            Code Python template
        """
        input_readers = "\n".join(
            f'{ds.lower().replace("-", "_")}_df = dataiku.Dataset("{ds}").get_dataframe()'
            for ds in input_datasets
        )

        template = f'''# Recipe Python généré automatiquement
import dataiku
import pandas as pd

# Chargement des données
{input_readers}

# TODO: Transformation à implémenter
# Exemple :
# result_df = {input_datasets[0].lower().replace("-", "_")}_df.copy()
# result_df = result_df[result_df["column"] > 0]

# Pour l'instant, on copie le premier dataset
result_df = {input_datasets[0].lower().replace("-", "_")}_df.copy()

# Écriture du résultat
output_ds = dataiku.Dataset("{output_dataset}")
output_ds.write_with_schema(result_df)
'''
        return template
