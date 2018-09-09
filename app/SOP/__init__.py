
from flask import Blueprint

bp = Blueprint('SOP', __name__, template_folder='templates')

from app.SOP import forms, routes
