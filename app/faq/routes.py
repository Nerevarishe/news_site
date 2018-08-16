from flask import render_template, redirect, url_for
from flask_login import login_required
from flask_babel import _
from app import db
from app.faq.forms import FaqForm
from app.models import FaqPost
from app.faq import bp


#############################################
# FAQ section
###
@bp.route('/', methods=['GET', 'POST'])
def faq():
    faq_posts = FaqPost().query.order_by(FaqPost.timestamp.desc()).all()
    return render_template('faq.html', title=_('FAQ'), faq_posts=faq_posts)

@bp.route('/add_faq', methods=['GET', 'POST'])
@login_required
def add_faq():
    form = FaqForm()
    if form.validate_on_submit():
        faq = FaqPost(title=form.title.data, body=form.body.data)
        db.session.add(faq)
        db.session.commit()
        faq_id = faq.id
        return redirect(url_for('faq.faq'))
    return render_template('add_faq.html', title=_('Add FAQ'), form=form)

@bp.route('/del_faq/<faq_id>')
@login_required
def del_faq(faq_id):
    delete_faq_id = FaqPost.query.filter_by(id=faq_id).first()
    db.session.delete(delete_faq_id)
    db.session.commit()
    return redirect(url_for('faq.faq'))
    
@bp.route('/edit_faq/<faq_id>', methods=['GET', 'POST'])
@login_required
def edit_faq(faq_id):
    edit_faq_id = FaqPost.query.filter_by(id=faq_id).first()
    form = FaqForm(title=edit_faq_id.title, body=edit_faq_id.body)
    if form.validate_on_submit():
        edit_faq_id.title = form.title.data
        edit_faq_id.body = body=form.body.data
        db.session.commit()
        return redirect(url_for('faq.faq'))
    return render_template('add_faq.html', form=form)