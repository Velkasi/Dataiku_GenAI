"""
generator.py - Génération de recettes Dataiku avec GitHub Copilot / LLM

Ce module propose des templates de recettes Python prêts à l'emploi,
et des helpers pour créer/mettre à jour des recettes via l'API DSS.

Intégration Copilot :
  Ouvrez ce fichier dans VS Code avec Copilot activé.
  Décrivez votre transformation en commentaire et laissez Copilot compléter.
"""

import logging
from typing import Optional

from src.api.client import get_project

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Templates de recettes
# ---------------------------------------------------------------------------

RECIPE_TEMPLATE_PYTHON = '''\
# Recipe: {recipe_name}
# Inputs : {inputs}
# Output : {output}
# Généré automatiquement — personnalisez selon vos besoins

import dataiku
import pandas as pd

# --- Chargement des données d'entrée ---
{input_readers}

# --- Transformation (complétée par Copilot / votre logique) ---
# Décrivez ici ce que vous voulez faire, Copilot suggérera le code :
# Exemple : "Filtrer les lignes où age > 18 et calculer la moyenne par région"


# --- Écriture du résultat ---
{output_writer}
'''


def build_python_recipe(
    recipe_name: str,
    input_datasets: list[str],
    output_dataset: str,
) -> str:
    """
    Génère le code d'une recette Python Dataiku à partir de templates.

    Args:
        recipe_name: Nom de la recette.
        input_datasets: Liste des datasets d'entrée.
        output_dataset: Nom du dataset de sortie.

    Returns:
        Code Python de la recette prêt à copier dans DSS.
    """
    input_readers = "\n".join(
        f'{ds.lower()}_df = dataiku.Dataset("{ds}").get_dataframe()'
        for ds in input_datasets
    )
    output_writer = (
        f'output_ds = dataiku.Dataset("{output_dataset}")\n'
        f'output_ds.write_with_schema(result_df)'
    )
    code = RECIPE_TEMPLATE_PYTHON.format(
        recipe_name=recipe_name,
        inputs=", ".join(input_datasets),
        output=output_dataset,
        input_readers=input_readers,
        output_writer=output_writer,
    )
    logger.info("Template de recette '%s' généré.", recipe_name)
    return code


def create_python_recipe_in_dss(
    recipe_name: str,
    input_datasets: list[str],
    output_dataset: str,
    project_key: Optional[str] = None,
) -> None:
    """
    Crée une recette Python dans DSS via l'API.

    Args:
        recipe_name: Nom de la recette à créer.
        input_datasets: Datasets d'entrée existants dans le projet.
        output_dataset: Dataset de sortie (doit exister ou être managé).
        project_key: Clé du projet DSS.
    """
    project = get_project(project_key)
    code = build_python_recipe(recipe_name, input_datasets, output_dataset)

    builder = project.new_recipe("python", recipe_name)
    for ds in input_datasets:
        builder.with_input(ds)
    builder.with_output(output_dataset)

    recipe = builder.build()
    recipe.get_settings().set_code(code)
    recipe.get_settings().save()

    logger.info(
        "Recette '%s' créée dans le projet '%s'.",
        recipe_name, project_key or "défaut",
    )
