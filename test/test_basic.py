import unittest
from app import create_app
from flask import current_app
from config.app_config import TestingConfig
from pathlib import Path

class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])    

    def test_database(client):
        folder_tester = Path("./app/model.py").is_file()
        assert folder_tester