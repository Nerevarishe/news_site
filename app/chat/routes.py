
from flask import render_template, redirect, url_for
from flask_login import login_required
from flask_babel import _
from app import db
from app.chat.forms import ChatPanelForm
#from app.models import ChatPost
from app.chat import bp


@bp.route('/', methods=['GET', 'POST'])
def chat():
    form = ChatPanelForm()
    return render_template('chat.html', title=_('Chat'), form=form)
