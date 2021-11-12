from flask import Flask, current_app
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://admin:admin@cluster0.gtfd0.mongodb.net/courses'

with app.app_context():
    mongo = PyMongo(current_app)
    courses = mongo.db.courses
