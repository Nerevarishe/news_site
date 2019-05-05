from flask import Blueprint


bp = Blueprint('deferred', __name__, template_folder='templates')

from app.deferred import forms, routes
