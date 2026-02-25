"""
rotate_api_key.py - Rotation sécurisée de la clé API Dataiku

Bonne pratique de sécurité : renouvelez régulièrement votre clé API.
Ce script génère une nouvelle clé via l'API DSS et met à jour le .env.

Usage :
    python scripts/rotate_api_key.py

IMPORTANT : Nécessite que l'utilisateur DSS ait les droits de gestion des clés API.
"""

import sys
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dotenv import load_dotenv
from src.api.client import get_client, get_config
from src.utils.logger import setup_logging

logger = setup_logging("rotate_api_key")


def update_env_file(new_key: str, env_path: Path) -> None:
    """Met à jour DSS_API_KEY dans le fichier .env sans toucher aux autres variables."""
    content = env_path.read_text(encoding="utf-8")
    updated = re.sub(
        r"^DSS_API_KEY=.*$",
        f"DSS_API_KEY={new_key}",
        content,
        flags=re.MULTILINE,
    )
    env_path.write_text(updated, encoding="utf-8")
    logger.info(".env mis à jour avec la nouvelle clé API.")


def rotate_api_key() -> None:
    """Crée une nouvelle clé API DSS et met à jour le .env."""
    load_dotenv()
    config = get_config()
    client = get_client()

    # Récupère l'utilisateur courant
    auth_info = client.get_auth_info()
    user_login = auth_info.get("authIdentifier")
    if not user_login:
        raise RuntimeError("Impossible de déterminer l'utilisateur connecté.")

    logger.info("Rotation de la clé API pour l'utilisateur : %s", user_login)

    # Crée une nouvelle clé API
    user = client.get_user(user_login)
    new_key_obj = user.create_personal_api_key(label="VS Code - auto-rotated")
    new_key = new_key_obj["key"]

    # Met à jour le .env
    env_path = Path(__file__).resolve().parents[1] / ".env"
    if env_path.exists():
        update_env_file(new_key, env_path)
        print(f"\n  Nouvelle clé API créée et sauvegardée dans .env")
        print(f"  Ancienne clé toujours active — supprimez-la manuellement dans DSS.")
    else:
        print(f"\n  Nouvelle clé API : {new_key}")
        print("  ATTENTION : Ajoutez-la dans votre .env manuellement (fichier .env introuvable).")


if __name__ == "__main__":
    try:
        rotate_api_key()
    except Exception as exc:
        logger.error("Échec de la rotation : %s", exc)
        sys.exit(1)
