from flask import render_template, redirect, url_for
from flask_login import login_required
from flask_babel import _
from app import db
from app.deferred.forms import DeferredForm
from app.models import DeferredDrug
from app.deferred import bp


@bp.route('/', methods=['GET', 'POST'])
def deferred():
    form = DeferredForm()
    deferred_posts = DeferredDrug().query.order_by(DeferredDrug.drug_name.asc()).all()
    if form.validate_on_submit():
        deferred_drug = DeferredDrug(
            drug_name = form.drug_name.data,
            drug_amount = form.drug_amount.data,
            comment = form.comment.data
        )
        db.session.add(deferred_drug)
        db.session.commit()
        return redirect(url_for('deferred.deferred'))
    return render_template('deferred.html', title=_('Deferred Drugs'), deferred_posts=deferred_posts, form=form)


@bp.route('/delete_drug/<id>', methods=['GET', 'POST'])
@login_required
def delete_drug(id):
    delete_drug = DeferredDrug().query.filter_by(id=id).first()
    db.session.delete(delete_drug)
    db.session.commit()
    return redirect(url_for('deferred.deferred'))