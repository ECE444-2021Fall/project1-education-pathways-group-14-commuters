import pytest
import unittest
from .courses import *
from werkzeug.datastructures import ImmutableMultiDict

class Test_Map_Query_Params(unittest.TestCase):
    def test_map_query_params_empty(self):
        actual = map_query_params(ImmutableMultiDict([]))
        expected = {}
        self.assertDictEqual(actual, expected)

    def test_map_query_params1(self):
        actual = map_query_params(ImmutableMultiDict([
            ('keyword', 'software'), 
            ('Department', 'Edward S. Rogers Sr. Dept. of Electrical & Computer Engin.')
        ]))
        expected = {'keyword': ['software'], 'Department': ['Edward S. Rogers Sr. Dept. of Electrical & Computer Engin.']}
        self.assertDictEqual(actual, expected)

    def test_map_query_params2(self):
        actual = map_query_params(ImmutableMultiDict([
            ('Department', 'Computer Science'), 
            ('Department', 'Edward S. Rogers Sr. Dept. of Electrical & Computer Engin.'), # multiple departments
            ('keyword', 'software'), 
        ]))
        expected = {'keyword': ['software'], 'Department': ['Computer Science', 'Edward S. Rogers Sr. Dept. of Electrical & Computer Engin.']}
        self.assertDictEqual(actual, expected)

class Test_Create_Search_Filter(unittest.TestCase):
    maxDiff = None

    def test_create_filter_empty(self):
        dictionary = {}
        actual = create_search_filter(dictionary)
        expected = {}
        self.assertDictEqual(actual, expected)
    
    def test_create_filter1(self): # 1 category, 1 filter
        dictionary = {'Department': ['Edward S. Rogers Sr. Dept. of Electrical & Computer Engin.']}
        actual = create_search_filter(dictionary)
        expected = {'$and':[
                {'$or': [
                    {'Department': "Edward S. Rogers Sr. Dept. of Electrical & Computer Engin."},
                ]},
            ]}
        self.assertDictEqual(actual, expected)

    def test_create_filter2(self): # 1 category, 2 filters
        dictionary = {'Department': ['Computer Science', 'Edward S. Rogers Sr. Dept. of Electrical & Computer Engin.']}
        actual = create_search_filter(dictionary)
        expected = {'$and':[
                {'$or': [
                    {'Department': "Computer Science"},
                    {'Department': "Edward S. Rogers Sr. Dept. of Electrical & Computer Engin."},
                ]},
            ]}
        self.assertDictEqual(actual, expected)  

    def test_create_filter3(self): # added category 'keyword'
        dictionary = {'keyword': ['software'], 'Department': ['Computer Science', 'Edward S. Rogers Sr. Dept. of Electrical & Computer Engin.']}
        actual = create_search_filter(dictionary)
        expected = {'$and':[
                {'$or': [
                    {'Name': {'$regex': 'software', '$options': "i"}},
                    {'Code': {'$regex': 'software', '$options': "i"}},
                ]},
                {'$or': [
                    {'Department': "Computer Science"},
                    {'Department': "Edward S. Rogers Sr. Dept. of Electrical & Computer Engin."},
                ]},
            ]}
        self.assertDictEqual(actual, expected)  

    def test_create_filter4(self): # more than one filter for 'keyword'
        dictionary = {'keyword': ['software', 'intro'], 'Department': ['Computer Science', 'Edward S. Rogers Sr. Dept. of Electrical & Computer Engin.']}
        actual = create_search_filter(dictionary)
        expected = {'$and':[
                {'$or': [
                    {'Name': {'$regex': 'software', '$options': "i"}},
                    {'Code': {'$regex': 'software', '$options': "i"}},
                    {'Name': {'$regex': 'intro', '$options': "i"}},
                    {'Code': {'$regex': 'intro', '$options': "i"}},
                ]},
                {'$or': [
                    {'Department': "Computer Science"},
                    {'Department': "Edward S. Rogers Sr. Dept. of Electrical & Computer Engin."},
                ]},
            ]}
        self.assertDictEqual(actual, expected)  
    
    def test_create_filter5(self): # many filters
        dictionary = {
            'keyword': ['ece', 'Intro'], 
            'Department': ['Computer Science', 'Edward S. Rogers Sr. Dept. of Electrical & Computer Engin.'],
            'Division': ['Faculty of Applied Science & Engineering'],
            'Term': ['2022 Winter', '2021 Summer S']
        }
        actual = create_search_filter(dictionary)
        expected = {'$and':[
                {'$or': [
                    {'Name': {'$regex': 'ece', '$options': "i"}},
                    {'Code': {'$regex': 'ece', '$options': "i"}},
                    {'Name': {'$regex': 'Intro', '$options': "i"}},
                    {'Code': {'$regex': 'Intro', '$options': "i"}}
                ]},
                {'$or': [
                    {'Department': "Computer Science"},
                    {'Department': "Edward S. Rogers Sr. Dept. of Electrical & Computer Engin."}
                ]}, 
                {'$or': [
                    {'Division': 'Faculty of Applied Science & Engineering'}
                ]},
                {'$or': [
                    {'Term': "2022 Winter"},
                    {'Term': "2021 Summer S"}
                ]}
        ]}
        self.assertDictEqual(actual, expected)  
