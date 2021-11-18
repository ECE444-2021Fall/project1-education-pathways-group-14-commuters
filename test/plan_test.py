import unittest

from flask.globals import session
from app import create_app
from config.app_config import TestingConfig
from config.db_config import TestDBConfig

create_app(TestingConfig, TestDBConfig)

from app import *
from app.main.views import planner
from app.main.views import edit
from app.main.views import temp_plan
from flask import redirect

"""
Test if not logged in we get redirected to login page when accessing plan
"""
def test_planner_login():
    tester = app.test_client()
    response = tester.get("/plan", content_type="html/text")

    assert response.status_code == 302 and b'href="/login"' in response.data

"""
Test if logged in render the /plan page 
"""
def test_planner():
    with app.test_client() as c:
        with c.session_transaction() as session:
            session['username'] = 'admin'

    response = c.get("/plan", content_type="html/text")

    assert response.status_code == 200

