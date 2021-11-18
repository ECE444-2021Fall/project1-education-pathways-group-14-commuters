import os

class LocalDBConfig:
    MONGO_URI = os.environ.get('DATABASE_URL') or \
        'mongodb+srv://admin:admin@cluster0.gtfd0.mongodb.net/courses'
    
class TestDBConfig:
    MONGO_URI = os.environ.get('TEST_DATABASE_URL') or \
        'mongodb+srv://admin:admin@cluster0.gtfd0.mongodb.net/test'