import unittest
from app import create_app
from config.app_config import TestingConfig
from config.db_config import TestDBConfig

create_app(TestingConfig, TestDBConfig)

from app.main.search import search_url
from app.main.forms import CourseSearchForm
"""
These tests allows us to verify that the function returns a non empty JSON file with different set of inputs
The correctness of the JSON data is not verified automatically
"""

search = CourseSearchForm()
"""Test if the url is generated accordingly using a course code"""
def test_search_url():
    rv = search_url(code='ECE444H1')
    assert rv