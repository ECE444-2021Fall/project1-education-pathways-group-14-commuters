import unittest
from app import create_app
from app.model import vectorizer, course_vectors, G, df
from config.app_config import TestingConfig

class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

