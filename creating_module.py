import argparse
import os
from errno import EEXIST


# Парсим имя будущего модуля
parser = argparse.ArgumentParser(description='Create new module in News Portal Site')
parser.add_argument('string', help='name of module')

args = parser.parse_args()
module_name = args.string

# Создаём дирректорию модуля в папке app
directory = './app/' + module_name
try:
    os.makedirs(directory)
except OSError as e:
    if e.errno != EEXIST:
        raise

# Создаём директорию шаблонов модуля
try:
    os.makedirs(directory + '/templates')
except OSError as e:
    if e.errno != EEXIST:
        raise

# Создаём базовые файлы модуля
# __init__.py
f = open(directory + '/__init__.py', 'w')
f.write("""from flask import Blueprint


bp = Blueprint('""" + module_name + """', __name__, template_folder='templates')

from app.""" + module_name + """ import forms, routes
""")
f.close()

# routes.py
f = open(directory + '/routes.py', 'w')
f.write("""from flask import render_template, redirect, url_for
from flask_login import login_required
from flask_babel import _
from app import db
# from app.""" + module_name + """.forms import """ + module_name.capitalize() + """Form
# from app.models import """ + module_name.capitalize() + """Post
from app.""" + module_name + """ import bp


@bp.route('/', methods=['GET', 'POST'])
def """ + module_name + """():
    # """ + module_name + """_posts = """ + module_name.capitalize() + """Post().query.order_by(""" + module_name.capitalize() + """Post.timestamp.desc()).all()
    return render_template('""" + module_name + """.html', title=_('""" + module_name + """'))
""")
f.close()

# forms.py
f = open(directory + '/forms.py', 'w')
f.write("""from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField
from flask_babel import lazy_gettext as _l

    
class """ + module_name.capitalize() + """Form(FlaskForm):
    title = StringField(_l('Title'), validators=[DataRequired()])
    body = CKEditorField(_l('FAQ'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))
""")
f.close()

# html page
f = open(directory + '/templates/' + module_name + '.html', 'w')
f.write('''{% extends "base.html" %}
{% import 'bootstrap/wtf.html' as wtf %}

{% block action_menu %}

{% endblock %}

{% block app_content %}
    ''' + module_name + ''' module created!
{% endblock %}
''')

