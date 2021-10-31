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

class Test_Get_Original_Value(unittest.TestCase):
    def test_get_original_value_campus(self):
        actual = get_original_value('Campus', 'UTSG')
        expected = 'St. George'
        self.assertEqual(actual, expected)
    
    def test_get_original_value_division(self):
        actual = get_original_value('Division', 'ArtSci')
        expected = 'Faculty of Arts and Science'
        self.assertEqual(actual, expected)
    
    def test_get_original_value_department1(self):
        actual = get_original_value('Department', 'CMSSC')
        expected = 'Dept. of Computer & Mathematical Sci (UTSC)'
        self.assertEqual(actual, expected)
    
    def test_get_original_value_department2(self):
        actual = get_original_value('Department', 'SMC')
        expected = 'St. Michael\'s College' #special character
        self.assertEqual(actual, expected)
    
    def test_get_original_value_utsc_breadth(self):
        actual = get_original_value('UTSC Breadth', 'ns')
        expected = 'Natural Sciences'
        self.assertEqual(actual, expected)
    
    def test_get_original_value_apsc_electives(self):
        actual = get_original_value('APSC Electives', 'cs')
        expected = 'Complementary Studies'
        self.assertEqual(actual, expected)

    def test_get_original_value_utm_distribution(self):
        actual = get_original_value('UTM Distribution', 'scihum')
        expected = 'Science or Humanities'
        self.assertEqual(actual, expected)
    
    def test_get_original_value_arts_and_science_breadth(self):
        actual = get_original_value('Arts and Science Breadth', '1') # '1' is a string
        expected = '(1) Creative and Cultural Representation'
        self.assertEqual(actual, expected)

    def test_get_original_value_arts_and_science_distribution(self):
        actual = get_original_value('Arts and Science Distribution', 'sciss') # '1' is a string
        expected = 'Science or Social Science'
        self.assertEqual(actual, expected)

    def test_get_original_value_no_converting1(self):
        actual = get_original_value('Campus', 'gibberish')
        expected = 'gibberish'
        self.assertEqual(actual, expected)
    
    def test_get_original_value_no_converting2(self):
        actual = get_original_value('Weird Key', 'ECE')
        expected = 'ECE'
        self.assertEqual(actual, expected)

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

    def test_create_filter_with_keyword1(self): # added category 'keyword'
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

    def test_create_filter_with_keyword2(self): # more than one filter for 'keyword'
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
    
    def test_create_filter_many(self): # many filters
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

    def test_create_filter_with_courselevel1(self): # added 'Course Level'
        dictionary = {'Course Level': ['1'], 'Department': ['Computer Science', 'Edward S. Rogers Sr. Dept. of Electrical & Computer Engin.']}
        actual = create_search_filter(dictionary)
        expected = {'$and':[
                {'$or': [
                    {'Course Level': 1},
                ]},
                {'$or': [
                    {'Department': "Computer Science"},
                    {'Department': "Edward S. Rogers Sr. Dept. of Electrical & Computer Engin."},
                ]},
            ]}
        self.assertDictEqual(actual, expected)  

    def test_create_filter_with_courselevel2(self): # added 'Course Level'
        dictionary = {'Course Level': ['1', '2', '3'], 'Department': ['Computer Science', 'Edward S. Rogers Sr. Dept. of Electrical & Computer Engin.']}
        actual = create_search_filter(dictionary)
        expected = {'$and':[
                {'$or': [
                    {'Course Level': 1},
                    {'Course Level': 2},
                    {'Course Level': 3},
                ]},
                {'$or': [
                    {'Department': "Computer Science"},
                    {'Department': "Edward S. Rogers Sr. Dept. of Electrical & Computer Engin."},
                ]},
            ]}
        self.assertDictEqual(actual, expected)

    def test_create_filter_with_boolean1(self): # FASEAvailable
        dictionary = {'FASEAvailable': ['True'], 'Department': ['Computer Science', 'Edward S. Rogers Sr. Dept. of Electrical & Computer Engin.']}
        actual = create_search_filter(dictionary)
        expected = {'$and':[
                {'$or': [
                    {'FASEAvailable': True},
                ]},
                {'$or': [
                    {'Department': "Computer Science"},
                    {'Department': "Edward S. Rogers Sr. Dept. of Electrical & Computer Engin."},
                ]},
            ]}
        self.assertDictEqual(actual, expected)
    
    def test_create_filter_with_boolean1(self): # FASEAvailable and MaybeRestricted
        dictionary = {'FASEAvailable': ['True'], 'MaybeRestricted': ['False'], 'Department': ['Computer Science', 'Edward S. Rogers Sr. Dept. of Electrical & Computer Engin.']}
        actual = create_search_filter(dictionary)
        expected = {'$and':[
                {'$or': [
                    {'FASEAvailable': True},
                ]},
                {'$or': [
                    {'MaybeRestricted': False},
                ]},
                {'$or': [
                    {'Department': "Computer Science"},
                    {'Department': "Edward S. Rogers Sr. Dept. of Electrical & Computer Engin."},
                ]},
            ]}
        self.assertDictEqual(actual, expected)