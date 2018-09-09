
from flask import render_template, redirect, url_for
from flask_login import login_required
from flask_babel import _
from app import db
from app.SOP.forms import SOPForm
from app.models import SOPPost
from app.SOP import bp


@bp.route('/')
def SOP_list():
    SOP_posts = SOPPost().query.order_by(SOPPost.timestamp.desc()).all()
    return render_template('SOP_list.html', title=_('Standard Operating Procedure'), SOP_posts=SOP_posts)

@bp.route('/add_SOP', methods=['GET', 'POST'])
@login_required
def add_SOP():
    form = SOPForm()
    if form.validate_on_submit():
        sop = SOPPost(title=form.title.data, body=form.body.data)
        db.session.add(sop)
        db.session.commit()
        return redirect(url_for('SOP.SOP_list'))
    return render_template('add_SOP.html', title=_('Add SOP'), form=form)

@bp.route('/SOP/<SOP_id>')
def SOP(SOP_id):
    SOP = SOPPost.query.filter_by(id=SOP_id).first()
    return render_template('SOP.html', title=SOP.title, SOP=SOP)

@bp.route('/edit_SOP/<SOP_id>', methods=['GET', 'POST'])
@login_required
def edit_SOP(SOP_id):
    edit_SOP_id = SOPPost.query.filter_by(id=SOP_id).first()
    form = SOPForm(title=edit_SOP_id.title, body=edit_SOP_id.body )
    if form.validate_on_submit():
        edit_SOP_id.title = form.title.data
        edit_SOP_id.body = form.body.data
        db.session.commit()
        return redirect(url_for('SOP.SOP_list'))
    return render_template('add_SOP.html', title=_('Edit SOP'), form=form)
    
@bp.route('/delete_SOP/<SOP_id>')
@login_required
def delete_SOP(SOP_id):
    delete_SOP_id = SOPPost.query.filter_by(id=SOP_id).first()
    db.session.delete(delete_SOP_id)
    db.session.commit()
    return redirect(url_for('SOP.SOP_list'))