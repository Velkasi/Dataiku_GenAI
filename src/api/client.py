"""
client.py - Connexion sécurisée à Dataiku DSS via API

Ce module charge les credentials depuis .env (jamais en dur dans le code)
et expose un client réutilisable dans tout le projet.
"""

import os
import logging
from functools import lru_cache
from typing import Optional

import dataikuapi
from dataikuapi.dss.project import DSSProject
from dotenv import load_dotenv

# Charger le fichier .env depuis la racine du projet
load_dotenv()

logger = logging.getLogger(__name__)


class DataikuConfig:
    """Centralise et valide la configuration DSS."""

    def __init__(self):
        self.url: str = self._require("DSS_URL")
        self.api_key: str = self._require("DSS_API_KEY")
        self.project_key: str = os.getenv("DSS_PROJECT_KEY", "")
        self.ssl_verify: bool = os.getenv("DSS_SSL_VERIFY", "true").lower() == "true"
        self.timeout: int = int(os.getenv("DSS_TIMEOUT", "30"))

    @staticmethod
    def _require(key: str) -> str:
        value = os.getenv(key)
        if not value:
            raise EnvironmentError(
                f"Variable d'environnement manquante : '{key}'. "
                f"Vérifiez votre fichier .env (copiez .env.example)."
            )
        return value


@lru_cache(maxsize=1)
def get_config() -> DataikuConfig:
    """Retourne la configuration (singleton mis en cache)."""
    return DataikuConfig()


def get_client() -> dataikuapi.DSSClient:
    """
    Crée et retourne un client Dataiku DSS authentifié.

    Returns:
        dataikuapi.DSSClient: Client prêt à l'emploi.

    Raises:
        EnvironmentError: Si DSS_URL ou DSS_API_KEY sont absents du .env.
        ConnectionError: Si la connexion au serveur échoue.
    """
    config = get_config()

    logger.info("Connexion à Dataiku DSS : %s", config.url)

    client = dataikuapi.DSSClient(
        host=config.url,
        api_key=config.api_key,
    )

    # Désactiver la vérification SSL uniquement si explicitement demandé
    if not config.ssl_verify:
        logger.warning(
            "Vérification SSL désactivée — ne pas utiliser en production."
        )
        client._session.verify = False

    # Test de connectivité rapide
    try:
        client.get_auth_info()
        logger.info("Connexion établie avec succès.")
    except Exception as exc:
        raise ConnectionError(
            f"Impossible de se connecter à {config.url}. "
            f"Vérifiez l'URL, la clé API et l'accès réseau. Détail : {exc}"
        ) from exc

    return client


def get_project(project_key: Optional[str] = None) -> DSSProject:
    """
    Retourne un objet projet Dataiku.

    Args:
        project_key: Clé du projet. Si None, utilise DSS_PROJECT_KEY du .env.

    Returns:
        dataikuapi.DSSProject
    """
    config = get_config()
    key = project_key or config.project_key
    if not key:
        raise ValueError(
            "Aucune clé de projet fournie. "
            "Définissez DSS_PROJECT_KEY dans .env ou passez project_key en argument."
        )
    client = get_client()
    return client.get_project(key)
