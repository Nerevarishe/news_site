
from flask import Blueprint

bp = Blueprint('spravka', __name__, template_folder='templates')

from app.spravka import forms, routes
