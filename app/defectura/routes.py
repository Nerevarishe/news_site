
from flask import render_template, redirect, url_for
from flask_login import login_required
from flask_babel import _
from app import db
from app.defectura.forms import DefecturaForm
from app.models import DefecturaCard
from app.defectura import bp


@bp.route('/')
def defectura():
    form = DefecturaForm()
    defectura_cards = DefecturaCard().query.group_by(DefecturaCard.timestamp).all()
    return render_template('defectura.html', title=_('Defectura'), form=form, defectura_cards = defectura_cards)
