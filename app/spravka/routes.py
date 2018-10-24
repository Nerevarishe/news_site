
from flask import render_template, redirect, url_for
from flask_login import login_required
from flask_babel import _
from app import db
from app.spravka.forms import DrugstoreListForm, ServiceCenterList
from app.models import DrugstoreList, ServiceCenterList
from app.spravka import bp


@bp.route('/', methods=['GET', 'POST'])
def spravka():
    drugstore_list_form = DrugstoreListForm()
    if drugstore_list_form.validate_on_submit():
        add_drugstore = DrugstoreList(ds_name=drugstore_list_form.ds_name.data, \
                                      ds_adress=drugstore_list_form.ds_adress.data, \
                                      ds_worktime=drugstore_list_form.ds_worktime.data, \
                                      ds_phone=drugstore_list_form.ds_phone.data, \
                                      ds_ip_phone=drugstore_list_form.ds_ip_phone.data)
        db.session.add(add_drugstore)
        db.session.commit()
    drugstore_list = DrugstoreList().query.order_by(DrugstoreList.ds_name).all()
    return render_template('spravka.html', title=_('Reference Information'), drugstore_list_form=drugstore_list_form, drugstore_list=drugstore_list)
