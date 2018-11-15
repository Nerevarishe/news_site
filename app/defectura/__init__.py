from flask import Blueprint


bp = Blueprint('defectura', __name__, template_folder='templates')

from app.defectura import forms, routes
