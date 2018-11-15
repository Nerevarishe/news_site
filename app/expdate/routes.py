import os, xlrd
from datetime import datetime
from flask import render_template, redirect, request, url_for, json
from flask_login import login_required
from flask_babel import _
from app import app, db
from app import documents
from app.expdate.forms import ExpdateAddItemForm, UploadExpDateTable
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


@bp.route('/upload_table', methods=['GET', 'POST'])
def upload_table():
    form = UploadExpDateTable()
    if form.validate_on_submit():
        filename = documents.save(request.files['file'])
        wb_file = os.path.join(app.config['UPLOADED_DOCUMENTS_DEST'], filename)
        workbook = xlrd.open_workbook(wb_file)
        sheet = workbook.sheet_by_index(0)
        first_row = app.config['FIRST_ROW']
        for rowno in range(first_row, sheet.nrows - app.config['SUBSTR_ROW']):
            drug_exp_date = xlrd.xldate.xldate_as_datetime(sheet.cell(rowno, app.config['COL_DATE']).value, workbook.datemode)
            expdate_row = ExpdateTable()
            expdate_row.drug_name = sheet.cell(rowno, app.config['COL_DRUG_NAME']).value
            expdate_row.exp_date = drug_exp_date
            expdate_row.amount = sheet.cell(rowno, app.config['COL_AMOUNT']).value
            db.session.add(expdate_row)
            db.session.commit()
        os.remove(wb_file)
        return redirect(url_for('expdate.expdate'))
    return render_template('upload_table.html', title=_('Upload Table'), form=form)
    

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
