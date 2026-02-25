"""
test_connection.py - Tests unitaires de la connexion Dataiku DSS

Utilise des mocks pour tester sans connexion réelle au serveur.
Exécution : pytest tests/ -v
"""

import os
from unittest.mock import MagicMock, patch

import pytest


class TestDataikuConfig:
    """Tests de la configuration via variables d'environnement."""

    def test_config_loads_from_env(self, monkeypatch):
        monkeypatch.setenv("DSS_URL", "https://dss.test.local")
        monkeypatch.setenv("DSS_API_KEY", "test_key_123")

        # Réinitialise le cache pour les tests
        from src.api.client import get_config
        get_config.cache_clear()

        config = get_config()
        assert config.url == "https://dss.test.local"
        assert config.api_key == "test_key_123"
        assert config.ssl_verify is True

        get_config.cache_clear()

    def test_config_raises_if_url_missing(self, monkeypatch):
        monkeypatch.delenv("DSS_URL", raising=False)
        monkeypatch.setenv("DSS_API_KEY", "test_key")

        from src.api.client import get_config, DataikuConfig
        get_config.cache_clear()

        with pytest.raises(EnvironmentError, match="DSS_URL"):
            DataikuConfig()

        get_config.cache_clear()

    def test_config_raises_if_apikey_missing(self, monkeypatch):
        monkeypatch.setenv("DSS_URL", "https://dss.test.local")
        monkeypatch.delenv("DSS_API_KEY", raising=False)

        from src.api.client import get_config, DataikuConfig
        get_config.cache_clear()

        with pytest.raises(EnvironmentError, match="DSS_API_KEY"):
            DataikuConfig()

        get_config.cache_clear()

    def test_ssl_verify_false_from_env(self, monkeypatch):
        monkeypatch.setenv("DSS_URL", "https://dss.test.local")
        monkeypatch.setenv("DSS_API_KEY", "test_key")
        monkeypatch.setenv("DSS_SSL_VERIFY", "false")

        from src.api.client import get_config, DataikuConfig
        get_config.cache_clear()

        config = DataikuConfig()
        assert config.ssl_verify is False

        get_config.cache_clear()


class TestGetClient:
    """Tests du client Dataiku avec mock de l'API."""

    @patch("src.api.client.dataikuapi.DSSClient")
    def test_get_client_success(self, mock_dss_class, monkeypatch):
        monkeypatch.setenv("DSS_URL", "https://dss.test.local")
        monkeypatch.setenv("DSS_API_KEY", "test_key")

        from src.api.client import get_config, get_client
        get_config.cache_clear()

        mock_client = MagicMock()
        mock_client.get_auth_info.return_value = {"authIdentifier": "user1"}
        mock_dss_class.return_value = mock_client

        client = get_client()
        assert client is mock_client
        mock_client.get_auth_info.assert_called_once()

        get_config.cache_clear()

    @patch("src.api.client.dataikuapi.DSSClient")
    def test_get_client_raises_on_connection_error(self, mock_dss_class, monkeypatch):
        monkeypatch.setenv("DSS_URL", "https://dss.test.local")
        monkeypatch.setenv("DSS_API_KEY", "bad_key")

        from src.api.client import get_config, get_client
        get_config.cache_clear()

        mock_client = MagicMock()
        mock_client.get_auth_info.side_effect = Exception("403 Forbidden")
        mock_dss_class.return_value = mock_client

        with pytest.raises(ConnectionError, match="Impossible de se connecter"):
            get_client()

        get_config.cache_clear()


class TestListProjects:
    """Tests de la liste des projets."""

    @patch("src.api.projects.get_client")
    def test_list_projects_returns_list(self, mock_get_client):
        mock_client = MagicMock()
        mock_client.list_projects.return_value = [
            {"projectKey": "PROJ_A", "name": "Projet Alpha"},
            {"projectKey": "PROJ_B", "name": "Projet Beta"},
        ]
        mock_get_client.return_value = mock_client

        from src.api.projects import list_projects
        result = list_projects()

        assert len(result) == 2
        assert result[0]["projectKey"] == "PROJ_A"

    @patch("src.api.projects.get_client")
    def test_list_projects_empty(self, mock_get_client):
        mock_client = MagicMock()
        mock_client.list_projects.return_value = []
        mock_get_client.return_value = mock_client

        from src.api.projects import list_projects
        result = list_projects()
        assert result == []
