import os
import unittest
from unittest.mock import patch

from app.config import get_settings


class SettingsTests(unittest.TestCase):
    def test_defaults_support_local_sqlite_without_ai_credentials(self):
        with patch.dict(os.environ, {}, clear=True):
            settings = get_settings()

        self.assertEqual(settings.database_url, "sqlite:///./app.db")
        self.assertIsNone(settings.nebius_api_key)
        self.assertIsNone(settings.nebius_model)

    def test_environment_values_override_defaults(self):
        values = {
            "DATABASE_URL": "sqlite:///./test.db",
            "NEBIUS_API_KEY": "test-key",
            "NEBIUS_BASE_URL": "https://example.invalid/v1/",
            "NEBIUS_MODEL": "test-model",
        }
        with patch.dict(os.environ, values, clear=True):
            settings = get_settings()

        self.assertEqual(settings.database_url, values["DATABASE_URL"])
        self.assertEqual(settings.nebius_api_key, values["NEBIUS_API_KEY"])
        self.assertEqual(settings.nebius_base_url, values["NEBIUS_BASE_URL"])
        self.assertEqual(settings.nebius_model, values["NEBIUS_MODEL"])
