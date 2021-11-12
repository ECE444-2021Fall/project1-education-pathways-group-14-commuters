# Unit tests
# Author: Shreya Rajendran
from __init__ import app

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
    response = tester.get("/search", content_type="html/text")

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

    assert b'logo.jpg' in response.data

def test_search_courses():
    """
    Ensure table is rendered
    """
    with app.test_client() as tester:
        response = tester.post("/", data=dict(search='computer',top='10',select='1', allow_redirects=True))
    assert response.status_code == 200
    assert b'table' in response.data
