# Tests for frontend and results table
# Author: Shreya Rajendran
import unittest
from app import create_app
from flask import current_app
from config.app_config import TestingConfig
from pathlib import Path


class appTestCases(unittest.TestCase):

    def setUp(self):
        """
        Set up the test client
        """
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)

    def test_index(self):
        """
        Check if index page is reachable
        """ 
        response = self.client.get("/", content_type="html/text")

        assert response.status_code == 200

    def test_search_url(self):
        """
        Check if search page is reachable
        """
        response = self.client.get("/find", content_type="html/text")

        assert response.status_code == 200

    def test_login_on_page(self):
        """
        Check if option to log in is available to user
        """
        response = self.client.get("/")

        assert b'Login' in response.data

    def test_search_on_page(self):
        """
        Check if search option is available to user
        """
        response = self.client.get("/")

        assert b'Search' in response.data

    def test_logo_on_page(self):
        """
        Ensure logo is displayed
        """
        response = self.client.get("/", content_type="html/text")

        assert b'logo' in response.data
        assert b'.png' in response.data

    def test_search_courses(self):
        """
        Ensure table is rendered
        """
        with self.client as tester:
            response = tester.post("/find", data=dict(search='computer',divisions='Faculty of Applied Science & Engineering',departments='Engineering First Year Office',campuses='St. George',top='10',select='1', allow_redirects=True))

        assert response.status_code == 200
        assert b'table' in response.data
        assert b'APS105H1' in response.data
        assert b'APS106H1' in response.data

    def test_no_result_courses(self):
        """
        Ensure no results message is displayed
        """
        with self.client as tester:
            response = tester.post("/find", data=dict(search='software',divisions='Faculty of Applied Science & Engineering',departments='Engineering First Year Office',campuses='St. George',top='10',select='1', allow_redirects=True))

        assert response.status_code == 200
        assert b'No Matching Results.' in response.data

    def test_planner_access(self):
        """
        Ensure no access to planner without login
        """
        with self.client as tester:
            response = tester.get("/plan")

        assert response.status_code == 302


    def test_login_access(self):
        """
        Check login username and password match cases
        """
        with self.client as tester:
            response = tester.post("/login", data=dict(username='admin', password='admin'))

        assert response.status_code == 200
        assert b'successfully logged in' in response.data

        with self.client as tester:
            response = tester.post("/login", data=dict(username='admin', password='a'))

        assert response.status_code == 200
        assert b'Invalid Credentials' in response.data
            

        with self.client as tester:
            response = tester.post("/login", data=dict(username='xyz', password='admin'))

        assert response.status_code == 200
        assert b'Invalid Credentials' in response.data