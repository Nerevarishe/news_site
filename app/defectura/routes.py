from flask import render_template, redirect, url_for, request, abort
from flask_login import login_required, current_user
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
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        add_string = DefecturaCard(drug_name=form.drug_name.data,
                                   comment=form.comment.data,
                                   employee_name=form.employee_name.data,
                                   date=date,
                                   ip=ip)
        db.session.add(add_string)
        db.session.commit()
    defectura_cards = DefecturaCard().query.filter_by(in_zd=False).order_by(DefecturaCard.date).all()
    defectura_cards_in_zd = DefecturaCard().query.filter_by(in_zd=True).order_by(DefecturaCard.date).all()
    return render_template('defectura.html', title=_('Defectura'), form=form, defectura_cards=defectura_cards,
                           defectura_cards_in_zd=defectura_cards_in_zd)


@bp.route('edit_item/<id>', methods=['GET', 'POST'])
def edit_item(id):
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    query = DefecturaCard.query.filter_by(id=id).first()
    # TODO: Переписать условия проверки на питоне:
    if query.ip != str(ip):
        if current_user.is_authenticated:
            if current_user.username == 'admin':
                pass
            else:
                return abort(401)
        elif current_user.is_anonymous:
            return abort(401)

    form = DefecturaForm(drug_name=query.drug_name,
                         comment=query.comment,
                         employee_name=query.employee_name)
    if form.validate_on_submit():
        date = datetime.utcnow()
        date = date.date()
        query.drug_name = form.drug_name.data
        query.comment = form.comment.data
        query.employee_name = form.employee_name.data
        query.date = date
        query.ip = ip
        db.session.commit()
        return redirect(url_for('defectura.defectura'))
    defectura_cards = DefecturaCard().query.order_by(DefecturaCard.date).all()
    return render_template('defectura_edit.html', title=_('Defectura'), form=form, defectura_cards=defectura_cards)


@bp.route('del_item/<id>')
def del_item(id):
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    query = DefecturaCard().query.filter_by(id=id).first()
    # TODO: Переписать условия проверки на питоне:
    if query.ip != str(ip):
        if current_user.is_authenticated:
            if current_user.username == 'admin':
                pass
            else:
                return abort(401)
        elif current_user.is_anonymous:
            return abort(401)

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


@bp.route('/add_to_zd/<id>')
@login_required
def add_to_zd(id):
    selected_card = DefecturaCard.query.filter_by(id=id).first()
    selected_card.in_zd = True
    db.session.commit()
    return redirect(url_for('defectura.defectura'))


@bp.route('/remove_from_zd/<id>')
@login_required
def remove_from_zd(id):
    selected_card = DefecturaCard.query.filter_by(id=id).first()
    selected_card.in_zd = False
    db.session.commit()
    return redirect(url_for('defectura.defectura'))
