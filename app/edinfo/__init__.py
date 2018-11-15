from flask import Blueprint


bp = Blueprint('edinfo', __name__, template_folder='templates')

from app.edinfo import forms, routes
