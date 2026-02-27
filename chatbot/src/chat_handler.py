"""
chat_handler.py - Gestionnaire de conversations avec Claude API

Gère les interactions avec Claude et l'exécution des commandes Dataiku.
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional
from anthropic import Anthropic

from dataiku_connector import get_connector
from workflow_builder import WorkflowBuilder
from prompts import get_system_prompt

logger = logging.getLogger(__name__)


class ChatHandler:
    """Gestionnaire de chat avec Claude API"""

    def __init__(self, project_key: Optional[str] = None):
        """
        Initialise le gestionnaire de chat.

        Args:
            project_key: Clé du projet Dataiku
        """
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY non définie dans .env")

        self.client = Anthropic(api_key=self.api_key)
        self.connector = get_connector(project_key)
        self.builder = WorkflowBuilder(self.connector)

        # Récupère les infos des datasets pour le prompt système
        self.datasets_info = self.connector.get_all_datasets_info()
        self.system_prompt = get_system_prompt(
            self.connector.project_key,
            self.datasets_info
        )

        logger.info(f"ChatHandler initialisé pour projet {self.connector.project_key}")

    def get_tools(self) -> List[Dict[str, Any]]:
        """
        Définit les outils disponibles pour Claude.

        Returns:
            Liste des outils (function tools)
        """
        return [
            {
                "name": "list_datasets",
                "description": "Liste tous les datasets disponibles dans le projet Dataiku avec leurs schémas",
                "input_schema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "get_dataset_info",
                "description": "Récupère les informations détaillées d'un dataset spécifique (colonnes, types, etc.)",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "dataset_name": {
                            "type": "string",
                            "description": "Nom du dataset à analyser"
                        }
                    },
                    "required": ["dataset_name"]
                }
            },
            {
                "name": "create_workflow",
                "description": "Crée un workflow complet dans Dataiku (datasets + recettes). À utiliser UNIQUEMENT après confirmation de l'utilisateur.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "workflow_name": {
                            "type": "string",
                            "description": "Nom descriptif du workflow"
                        },
                        "source_datasets": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Liste des datasets sources utilisés"
                        },
                        "recipes": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "type": {"type": "string", "enum": ["python", "grouping", "join"]},
                                    "name": {"type": "string"},
                                    "inputs": {"type": "array", "items": {"type": "string"}},
                                    "input": {"type": "string"},
                                    "output": {"type": "string"},
                                    "group_by": {"type": "array", "items": {"type": "string"}},
                                    "aggregations": {"type": "array"}
                                }
                            },
                            "description": "Liste des recettes à créer dans l'ordre"
                        },
                        "output_dataset": {
                            "type": "string",
                            "description": "Nom du dataset final créé"
                        }
                    },
                    "required": ["workflow_name", "source_datasets", "recipes", "output_dataset"]
                }
            }
        ]

    def execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> Any:
        """
        Exécute un outil demandé par Claude.

        Args:
            tool_name: Nom de l'outil
            tool_input: Paramètres de l'outil

        Returns:
            Résultat de l'exécution
        """
        logger.info(f"Exécution outil : {tool_name}")

        try:
            if tool_name == "list_datasets":
                datasets = self.connector.get_available_datasets()
                datasets_with_info = []
                for ds in datasets:
                    info = self.connector.get_dataset_info(ds)
                    datasets_with_info.append({
                        "name": ds,
                        "columns": [f"{c['name']} ({c['type']})" for c in info['columns']]
                    })
                return {"datasets": datasets_with_info}

            elif tool_name == "get_dataset_info":
                dataset_name = tool_input["dataset_name"]
                info = self.connector.get_dataset_info(dataset_name)
                return info

            elif tool_name == "create_workflow":
                result = self.builder.create_workflow(
                    workflow_name=tool_input["workflow_name"],
                    source_datasets=tool_input["source_datasets"],
                    recipes=tool_input["recipes"],
                    output_dataset=tool_input["output_dataset"]
                )
                return result

            else:
                return {"error": f"Outil inconnu : {tool_name}"}

        except Exception as e:
            logger.error(f"Erreur exécution outil {tool_name} : {e}")
            return {"error": str(e)}

    def process_message(
        self,
        user_message: str,
        conversation_history: List[Dict[str, Any]]
    ) -> tuple[str, List[Dict[str, Any]]]:
        """
        Traite un message utilisateur et retourne la réponse de Claude.

        Args:
            user_message: Message de l'utilisateur
            conversation_history: Historique de la conversation

        Returns:
            Tuple (réponse, historique_mis_à_jour)
        """
        # Ajoute le message utilisateur
        messages = conversation_history + [
            {"role": "user", "content": user_message}
        ]

        # Boucle pour gérer les tool uses
        while True:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4096,
                system=self.system_prompt,
                messages=messages,
                tools=self.get_tools()
            )

            # Traite la réponse
            if response.stop_reason == "end_turn":
                # Fin normale, extrait le texte
                text_content = ""
                for block in response.content:
                    if hasattr(block, "text"):
                        text_content += block.text

                # Ajoute la réponse à l'historique
                messages.append({
                    "role": "assistant",
                    "content": response.content
                })

                return text_content, messages

            elif response.stop_reason == "tool_use":
                # Claude veut utiliser un outil
                tool_results = []
                assistant_content = []

                for block in response.content:
                    if block.type == "text":
                        assistant_content.append(block)
                    elif block.type == "tool_use":
                        assistant_content.append(block)

                        # Exécute l'outil
                        result = self.execute_tool(block.name, block.input)

                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(result, ensure_ascii=False)
                        })

                # Ajoute la réponse de l'assistant et les résultats des outils
                messages.append({
                    "role": "assistant",
                    "content": assistant_content
                })
                messages.append({
                    "role": "user",
                    "content": tool_results
                })

                # Continue la boucle pour obtenir la réponse finale

            else:
                # Autre stop_reason
                return f"Réponse inattendue : {response.stop_reason}", messages


def create_chat_handler(project_key: Optional[str] = None) -> ChatHandler:
    """
    Factory function pour créer un gestionnaire de chat.

    Args:
        project_key: Clé du projet Dataiku

    Returns:
        Instance de ChatHandler
    """
    return ChatHandler(project_key)
