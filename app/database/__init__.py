from flask import Blueprint

database = Blueprint('courses_dp', __name__)

from . import courses, users