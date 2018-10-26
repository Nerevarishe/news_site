from flask import render_template, redirect, url_for
from flask_login import login_required
from flask_babel import _
from app import db
from app.spravka.forms import DrugstoreListForm, ServiceCenterListForm
from app.models import DrugstoreList, ServiceCenterList
from app.spravka import bp


@bp.route('/', methods=['GET', 'POST'])
def spravka():
    drugstore_list = DrugstoreList().query.order_by(DrugstoreList.ds_name).all()
    sc_list = ServiceCenterList().query.order_by(ServiceCenterList.brands).all()
    return render_template('spravka.html', title=_('Reference Information'), drugstore_list=drugstore_list, sc_list=sc_list)


@bp.route('/add_drugstore', methods=['GET', 'POST'])
@login_required
def add_drugstore():
    form = DrugstoreListForm()
    if form.validate_on_submit():
        add_drugstore = DrugstoreList(ds_name=form.ds_name.data,
                                      ds_adress=form.ds_adress.data,
                                      ds_worktime=form.ds_worktime.data,
                                      ds_phone=form.ds_phone.data,
                                      ds_ip_phone=form.ds_ip_phone.data)
        db.session.add(add_drugstore)
        db.session.commit()
        return redirect(url_for('spravka.spravka'))
    return render_template('add_drugstore.html', title=_('Add Drugstore'), form=form)


@bp.route('/edit_drugstore/<id>', methods=['GET', 'POST'])
@login_required
def edit_drugstore(id):
    edit_drugstore = DrugstoreList().query.filter_by(id=id).first()
    form = DrugstoreListForm(ds_name=edit_drugstore.ds_name,
                             ds_adress=edit_drugstore.ds_adress,
                             ds_worktime=edit_drugstore.ds_worktime,
                             ds_phone=edit_drugstore.ds_phone,
                             ds_ip_phone=edit_drugstore.ds_ip_phone)
    if form.validate_on_submit():
        edit_drugstore.ds_name = form.ds_name.data
        edit_drugstore.ds_adress = form.ds_adress.data
        edit_drugstore.ds_worktime = form.ds_worktime.data
        edit_drugstore.ds_phone = form.ds_phone.data
        edit_drugstore.ds_ip_phone = form.ds_ip_phone.data
        db.session.commit()
        return redirect(url_for('spravka.spravka'))
    return render_template('add_drugstore.html', title=_('Edit Drugstore Info'), form=form)


@bp.route('/del_drugstore/<id>', methods=['GET', 'POST'])
@login_required
def del_drugstore(id):
    del_drugstore = DrugstoreList().query.filter_by(id=id).first()
    db.session.delete(del_drugstore)
    db.session.commit()
    return redirect(url_for('spravka.spravka'))


@bp.route('/add_SC', methods=['GET', 'POST'])
@login_required
def add_sc():
    form = ServiceCenterListForm()
    if form.validate_on_submit():
        add_sc = ServiceCenterList(brands=form.brands.data,
                                   sc_adress=form.sc_adress.data,
                                   sc_phone=form.sc_phone.data)
        db.session.add(add_sc)
        db.session.commit()
        return redirect(url_for('spravka.spravka'))
    return render_template('add_sc.html', title=_('Add new Service Center'), form=form)


@bp.route('/edit_SC/<id>', methods=['GET', 'POST'])
@login_required
def edit_sc(id):
    edit_sc = ServiceCenterList().query.filter_by(id=id).first()
    form = ServiceCenterListForm(brands=edit_sc.brands,
                                 sc_adress=edit_sc.sc_adress,
                                 sc_phone=edit_sc.sc_phone)
    if form.validate_on_submit():
        edit_sc.brands = form.brands.data
        edit_sc.sc_adress = form.sc_adress.data
        edit_sc.sc_phone = form.sc_phone.data
        db.session.commit()
        return redirect(url_for('spravka.spravka'))
    return render_template('add_sc.html', title=_('Edit Service Center'), form=form)


@bp.route('/del_SC/<id>', methods=['GET', 'POST'])
@login_required
def del_sc(id):
    del_sc = ServiceCenterList().query.filter_by(id=id).first()
    db.session.delete(del_sc)
    db.session.commit()
    return redirect(url_for('spravka.spravka'))
