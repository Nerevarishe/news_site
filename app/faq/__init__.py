from flask import Blueprint

bp = Blueprint('faq', __name__, template_folder='templates')

from app.faq import forms, routes