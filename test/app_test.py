# Tests for frontend and results table
# Author: Shreya Rajendran
import unittest
from app import create_app
from config.app_config import TestingConfig
from config.db_config import TestDBConfig

create_app(TestingConfig, TestDBConfig)

from app import *

def test_index():
    """
    Check if index page is reachable
    """ 
    tester = app.test_client()
    response = tester.get("/", content_type="html/text")

    assert response.status_code == 200

def test_search_url():
    """
    Check if search page is reachable
    """
    tester = app.test_client()
    response = tester.get("/find", content_type="html/text")

    assert response.status_code == 200

def test_login_on_page():
    """
    Check if option to log in is available to user
    """
    tester = app.test_client()
    response = tester.get("/")

    assert b'Login' in response.data

def test_search_on_page():
    """
    Check if search option is available to user
    """
    tester = app.test_client()
    response = tester.get("/")

    assert b'Search' in response.data

def test_logo_on_page():
    """
    Ensure logo is displayed
    """
    tester = app.test_client()
    response = tester.get("/")

    assert b'logo' in response.data
    assert b'.png' in response.data


def test_search_courses():
        """
        Ensure table is rendered
        """
        with app.test_client() as tester:
            response = tester.post("/find", data=dict(search='computer',divisions='Faculty of Applied Science & Engineering',departments='Engineering First Year Office',campuses='St. George',top='10',select='1', allow_redirects=True))

        assert response.status_code == 200
        assert b'table' in response.data
        assert b'APS105H1' in response.data
        assert b'APS106H1' in response.data

def test_no_result_courses():
    """
    Ensure no results message is displayed
    """
    with app.test_client() as tester:
        response = tester.post("/find", data=dict(search='software',divisions='Faculty of Applied Science & Engineering',departments='Engineering First Year Office',campuses='St. George',top='10',select='1', allow_redirects=True))

    assert response.status_code == 200
    assert b'No Matching Results.' in response.data

def test_planner_access():
    """
    Ensure no access to planner without login
    """
    with app.test_client() as tester:
        response = tester.get("/plan")

    assert response.status_code == 302


def test_login_access():
    """
    Check login username and password match cases
    """
    with app.test_client() as tester:
        response = tester.post("/login", data=dict(username='admin', password='admin'))

    assert response.status_code == 200
    assert b'successfully logged in' in response.data

    with app.test_client() as tester:
        response = tester.post("/login", data=dict(username='admin', password='a'))

    assert response.status_code == 200
    assert b'Invalid Credentials' in response.data
        

    with app.test_client() as tester:
        response = tester.post("/login", data=dict(username='xyz', password='admin'))

    assert response.status_code == 200
    assert b'Invalid Credentials' in response.data
