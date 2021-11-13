import search

def test_search_url():
    """Test if the url is generated accordingly using more than 1 filter"""
    #(tags, year, division, department, campus)
    rv = search.search_url("Any", 2, "Any", "Edward S. Rogers Sr. Dept. of Electrical & Computer Engin.", "Any")
    assert rv == "/api/course/search?Department=ece&Course+Level=2"

""""""
"""Tests if the url is generated accordingly for each different filters one by one"""
""""""
def test_search_url_tags():
    #(tags, year, division, department, campus)
    rv = search.search_url("software", "Any", "Any", "Any", "Any")
    assert rv == "/api/course/search?keyword=software"

def test_search_url_year():
    #(tags, year, division, department, campus)
    rv = search.search_url("Any", 2, "Any", "Any", "Any")
    assert rv == "/api/course/search?Course+Level=2"

def test_search_url_division():
    #(tags, year, division, department, campus)
    rv = search.search_url("Any", "Any", "Faculty of Music", "Any", "Any")
    assert rv == "/api/course/search?Division=music"

def test_search_url_department():
    #(tags, year, division, department, campus)
    rv = search.search_url("Any", "Any", "Any", "Edward S. Rogers Sr. Dept. of Electrical & Computer Engin.", "Any")
    assert rv == "/api/course/search?Department=ece"

def test_search_url_campus():
    #(tags, year, division, department, campus)
    rv = search.search_url("Any", "Any", "Any", "Any", "Mississauga")
    assert rv == "/api/course/search?Campus=utm"
""""""
""""""
""""""

"""Test if the url is generated accordingly without any filters applied"""
def test_search_url_no_filters():
    #(tags, year, division, department, campus)
    rv = search.search_url("Any", "Any", "Any", "Any", "Any")
    assert rv == "/api/course/search?"