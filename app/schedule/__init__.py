from flask import Blueprint


bp = Blueprint('schedule', __name__, template_folder='templates')

from app.schedule import forms, routes
