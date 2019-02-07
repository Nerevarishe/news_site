from flask import render_template, redirect, url_for
from flask_login import login_required
from flask_babel import _
from app import db
from app.orders.forms import LawForm
from app.models import News, LawPost
from app.orders import bp


#############################################
# Orders section
#
@bp.route('/', methods=['GET', 'POST'])
def orders():
    law_posts = LawPost().query.order_by(LawPost.timestamp.desc()).all()
    return render_template('orders.html', title=_('Orders'), law_posts=law_posts)


@bp.route('/law/<law_id>')
def law(law_id):
    law = LawPost().query.filter_by(id=law_id).first()
    return render_template('law.html', title=law.title, law=law)


@bp.route('/add_law', methods=['GET', 'POST'])
@login_required
def add_law():
    form = LawForm()
    if form.validate_on_submit():
        law = LawPost(title=form.title.data, body=form.body.data)
        db.session.add(law)
        db.session.commit()
        if form.add_to_news.data is True:
            news = News(
                body=_('Added new order') + '<br><a href="' + url_for('orders.law', law_id=law.id, _external=True)
                     + '">' + form.title.data + '</a>',
                source='ORD-' + str(law.id)
            )
            db.session.add(news)
            db.session.commit()
        return redirect(url_for('orders.orders'))
    return render_template('add_law.html', title=_('Add law'), form=form)


@bp.route('/del_law/<law_id>')
@login_required
def del_law(law_id):
    delete_law_id = LawPost.query.filter_by(id=law_id).first()
    find_news = News.query.filter_by(source='ORD-' + str(delete_law_id.id)).all()
    for post in find_news:
        db.session.delete(post)
        db.session.commit()
    db.session.delete(delete_law_id)
    db.session.commit()
    return redirect(url_for('orders.orders'))


@bp.route('/edit_law/<law_id>', methods=['GET', 'POST'])
@login_required
def edit_law(law_id):
    edit_law_id = LawPost.query.filter_by(id=law_id).first()
    form = LawForm(title=edit_law_id.title, body=edit_law_id.body)
    if form.validate_on_submit():
        edit_law_id.title = form.title.data
        edit_law_id.body = form.body.data
        db.session.commit()
        if form.add_to_news.data is True:
            news = News(
                body=_('Order updated:') + '<br><a href="' + url_for('orders.law', law_id=edit_law_id.id, _external=True) + '">' + form.title.data + '</a>',
                source='ORD-' + str(edit_law_id.id)
            )
            db.session.add(news)
            db.session.commit()
        return redirect(url_for('orders.orders'))
    return render_template('add_law.html', form=form)
