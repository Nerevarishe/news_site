from datetime import datetime
from flask import render_template, redirect, url_for, json
from flask_login import login_required
from flask_babel import _
from app import db
from app.expdate.forms import ExpdateAddItemForm
from app.models import ExpdateTable
from app.expdate import bp


@bp.route('/')
def expdate():
    expdate_table = ExpdateTable.query.order_by(ExpdateTable.exp_date.asc()).all()
    form = ExpdateAddItemForm()
    return render_template('expdate.html', title=_('Exp. Dates'), expdate_table=expdate_table)

@bp.route('/add_exp_date', methods=['GET', 'POST'])
@login_required
def add_exp_date():
    form = ExpdateAddItemForm()
    if form.validate_on_submit():
        exp_date_item = ExpdateTable(drug_name=form.drug_name.data, exp_date=form.exp_date.data, amount=form.amount.data)
        db.session.add(exp_date_item)
        db.session.commit()
        return redirect(url_for('expdate.expdate'))
    return render_template('add_exp_date.html', title=_('Add Exp. Date'), form=form)

@bp.route('/del_exp_date/<row_id>')
@login_required
def del_exp_date(row_id):
    row_id = ExpdateTable.query.filter_by(id=row_id).first()
    db.session.delete(row_id)
    db.session.commit()
    return redirect(url_for('expdate.expdate'))

@bp.route('/_inc_amount/<row_id>', methods=['POST'])
def _inc_amount(row_id):
    row_id = ExpdateTable.query.filter_by(id=row_id).first()
    row_id.amount += 1
    db.session.commit()
    return json.dumps({'amount': row_id.amount})
    
@bp.route('/_dec_amount/<row_id>', methods=['POST'])
def _dec_amount(row_id):
    row_id = ExpdateTable.query.filter_by(id=row_id).first()
    if row_id.amount > 0:
        row_id.amount -= 1
        db.session.commit()
    return json.dumps({'amount': row_id.amount})