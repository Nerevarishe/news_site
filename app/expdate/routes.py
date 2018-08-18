
from flask import render_template, redirect, url_for
from flask_login import login_required
from flask_babel import _
from app import db
#from app.expdate.forms import ExpdateForm
from app.models import ExpdateTable
from app.expdate import bp


@bp.route('/', methods=['GET', 'POST'])
def expdate():
    #expdate_posts = ExpdateTable().query.order_by(ExpdateTable.timestamp.desc()).all()
    return render_template('expdate.html', title=_('expdate'))
