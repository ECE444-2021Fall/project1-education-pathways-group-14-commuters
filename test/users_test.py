import unittest
from app import create_app
from config.app_config import TestingConfig
from config.db_config import TestDBConfig

create_app(TestingConfig, TestDBConfig)
from app.database.users import *

def insertDoc(new):
    # insert a new document
    users.insert_one(new)

def deleteAllDocs():
    # delete all documents in the collection
    users.delete_many({})

class TestNewUser(unittest.TestCase):
    def testNewUserWrongYearType(self):
        deleteAllDocs() # prepare db
        actual = newUser("test", "testName", "testEmail", "10041111111", "UTSG", "APSC", "ECE", 4, "FT", "2020", 2025, "password")
        expected = False
        self.assertEqual(actual, expected)
    
    def testNewUserWrongStartYearType(self):
        deleteAllDocs() # prepare db
        actual = newUser("test", "testName", "testEmail", "10041111111", "UTSG", "APSC", "ECE", 4, "FT", "2020", 2025, "password")
        expected = False
        self.assertEqual(actual, expected)
    
    def testNewUserWrongGradYearType(self):
        deleteAllDocs() # prepare db
        actual = newUser("test", "testName", "testEmail", "10041111111", "UTSG", "APSC", "ECE", 4, "FT", 2021, "2025", "password")
        expected = False
        self.assertEqual(actual, expected)

    def testNewUserSuccess(self):
        deleteAllDocs() # prepare db
        actual = newUser("test", "testName", "testEmail", "10041111111", "UTSG", "APSC", "ECE", 4, "FT", 2021, 2025, "password")
        expected = True
        self.assertEqual(actual, expected)

class TestGetUser(unittest.TestCase):
    def testGetUserNoSuchUser(self):
        deleteAllDocs() # prepare db
        actual = getUser("gibberish")
        expected = None
        self.assertEqual(actual, expected)

    def testGetUserSucess(self):
        # prepare db
        deleteAllDocs()
        newUser = {
            '_id': 'testUser', 
            'name': ' Test User', 
            'email': 'test@mail.utoronto.ca', 
            'studentNumber': '1234567890', 
            'campus': 'UTSG', 
            'division': 'APSC', 
            'department': 'ECE', 
            'year': 1, 
            'status': 'FT', 
            'startYear': 2020, 
            'gradYear': 2024, 
            'plan': {
                '2020F': [], '2021W': [], '2021S': [], '2021F': [], 
                '2022W': ['ECE216H1', 'ECE221H1', 'ECE231H1', 'MUS243H1', 'ECE297'], 
                '2022S': [], '2022F': [], '2023W': [], '2023S': [], '2023F': [], '2024W': [], '2024S': []
            }, 
            'password': '1234'
        }
        insertDoc(newUser)
        # execute
        actual = getUser("testUser")
        expected = newUser
        self.assertDictEqual(actual, expected)

class TestIsCorrectPassword(unittest.TestCase):
    def testIsCorrectPasswordTrue(self):
        # prepare db
        deleteAllDocs()
        newUser = {
            '_id': 'testUser',
            'password': '1234'
        }
        insertDoc(newUser) 
        # execute
        actual = isCorrectPassword("testUser", "1234")
        expected = True
        self.assertEqual(actual, expected)

    def testIsCorrectPasswordFalse(self):
        # prepare db
        deleteAllDocs()
        newUser = {
            '_id': 'testUser',
            'password': '1234'
        }
        insertDoc(newUser) 
        # execute
        actual = isCorrectPassword("testUser", "gibberish")
        expected = False
        self.assertEqual(actual, expected)

class TestGetPlan(unittest.TestCase):
    def testGetPlanNoSuchUser(self):
        # prepare db
        deleteAllDocs()
        user = {
            '_id': 'testUser',
            'plan': {
                '2020F': [], '2021W': [], '2021S': [], '2021F': [], '2022W': [], '2022S': [],
                '2022F': [], '2023W': [], '2023S': [], '2023F': [], '2024W': [], '2024S': []
            }, 
        }
        insertDoc(user)
        # execute
        actual = getPlan("gibberish")
        expected = None
        self.assertEqual(actual, expected)
    
    def testGetPlanSuccess(self):
        # prepare db
        deleteAllDocs()
        user = {
            '_id': 'testUser',
            'plan': {
                '2020F': [], '2021W': [], '2021S': [], '2021F': [], '2022W': [], '2022S': [],
                '2022F': [], '2023W': [], '2023S': [], '2023F': [], '2024W': ['ECE318H1', 'ECE528H1', 'CSC343H1', 'ECE472'], '2024S': []
            }, 
        }
        insertDoc(user)
        #execute
        actual = getPlan("testUser")
        expected = user.get("plan")
        self.assertEqual(actual, expected)
    
class TestUpdatePlan(unittest.TestCase):
    def testUpdatePlanNotDictionary(self):
        # prepare db
        deleteAllDocs()
        user = {
            '_id': 'testUser',
            'plan': {
                '2020F': [], '2021W': [], '2021S': [], '2021F': [], '2022W': [], '2022S': [],
                '2022F': [], '2023W': [], '2023S': [], '2023F': [], '2024W': [], '2024S': []
            }, 
        }
        insertDoc(user)
        #execute
        planWithWrongType = 3
        actual = updatePlan("testUser", planWithWrongType)
        expected = False
        self.assertEqual(actual, expected)
    
    def testUpdatePlanNoSuchUser(self):
        # prepare db
        deleteAllDocs()
        plan = {
            '2020F': [], '2021W': [], '2021S': [], '2021F': [], '2022W': [], '2022S': [],
            '2022F': [], '2023W': [], '2023S': [], '2023F': [], '2024W': [], '2024S': []
        }
        #execute
        actual = updatePlan("gibberish", plan)
        expected = False
        self.assertEqual(actual, expected)

    def testUpdatePlanSuccess(self):
         # prepare db
        deleteAllDocs()
        user = {
            '_id': 'testUser',
            'plan': {
                '2020F': [], '2021W': [], '2021S': [], '2021F': [], '2022W': [], '2022S': [],
                '2022F': [], '2023W': [], '2023S': [], '2023F': [], '2024W': [], '2024S': []
            }, 
        }
        insertDoc(user)
        #execute
        newPlan = {
            '2020F': [], '2021W': [], '2021S': [], '2021F': [], '2022W': [], '2022S': [],
            '2022F': ['ECE318H1', 'ECE528H1', 'CSC343H1', 'ECE472'], '2023W': [], '2023S': [], '2023F': [], '2024W': [], '2024S': []
        }
        actual = updatePlan("testUser", newPlan)
        expected = True
        self.assertEqual(actual, expected)