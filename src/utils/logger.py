"""
logger.py - Configuration du logging pour le projet

Configure un logger structuré avec niveau défini via .env (LOG_LEVEL).
À importer en premier dans les scripts principaux.
"""

import logging
import os
import sys
from pathlib import Path


def setup_logging(name: str = "dataiku_project") -> logging.Logger:
    """
    Configure et retourne un logger applicatif.

    Args:
        name: Nom du logger (identifie la source dans les logs).

    Returns:
        logging.Logger configuré.
    """
    level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_str, logging.INFO)

    # Créer le dossier logs/ si nécessaire
    log_dir = Path(__file__).resolve().parents[2] / "logs"
    log_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_dir / "dataiku_project.log", encoding="utf-8"),
        ],
    )

    logger = logging.getLogger(name)
    logger.info("Logging initialisé (niveau : %s).", level_str)
    return logger
