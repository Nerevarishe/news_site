
from flask import Blueprint

bp = Blueprint('expdate', __name__, template_folder='templates')

from app.expdate import forms, routes
