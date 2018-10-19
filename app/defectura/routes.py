from flask import render_template, redirect, url_for
from flask_login import login_required
from flask_babel import _
from app import db
from app.defectura.forms import DefecturaForm
from app.models import DefecturaCard
from app.defectura import bp
from datetime import datetime


@bp.route('/', methods=['GET', 'POST'])
def defectura():
    form = DefecturaForm()
    if form.validate_on_submit():
        date = datetime.utcnow()
        date = date.date()
        add_string = DefecturaCard(drug_name=form.drug_name.data, date=date)
        db.session.add(add_string)
        db.session.commit()
    defectura_cards = DefecturaCard().query.order_by(DefecturaCard.date).all()
    return render_template('defectura.html', title=_('Defectura'), form=form, defectura_cards=defectura_cards)
    

@bp.route('del_item/<id>')
def del_item(id):
    query = DefecturaCard().query.filter_by(id=id).first()
    db.session.delete(query)
    db.session.commit()
    return redirect(url_for('defectura.defectura'))


@bp.route('/delete_card/<date>')
@login_required
def delete_card(date):
    select_cards = DefecturaCard().query.filter_by(date=date).all()
    for item in select_cards:
        q = DefecturaCard().query.filter_by(id=item.id).first()
        db.session.delete(q)
        db.session.commit()
    return redirect(url_for('defectura.defectura'))
