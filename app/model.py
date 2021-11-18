from flask_pymongo import PyMongo
from . import app

mongo = PyMongo(app)
courses = mongo.db.courses
users = mongo.db.users


