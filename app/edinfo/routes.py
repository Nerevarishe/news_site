from flask import render_template, redirect, url_for
from flask_login import login_required
from flask_babel import _
from app import db
from app.edinfo.forms import EdinfoForm
from app.models import EdinfoPost
from app.edinfo import bp


@bp.route('/')
def edinfo():
    edinfo_posts = EdinfoPost().query.order_by(EdinfoPost.timestamp.desc()).all()
    return render_template('articles_list.html', title=_('Education Information'), edinfo_posts=edinfo_posts)


@bp.route('/article/<article_id>')
def article(article_id):
    article = EdinfoPost.query.filter_by(id=article_id).first()
    return render_template('article.html', title=article.title, article=article)


@bp.route('/add_article', methods=['GET', 'POST'])
@login_required
def add_article():
    form = EdinfoForm()
    if form.validate_on_submit():
        article = EdinfoPost(title=form.title.data, body=form.body.data)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('edinfo.edinfo'))
    return render_template('add_article.html', title=_('Add article'), form=form)


@bp.route('/edit_article/<article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    edit_article_id = EdinfoPost.query.filter_by(id=article_id).first()
    form = EdinfoForm(title=edit_article_id.title, body=edit_article_id.body)
    if form.validate_on_submit():
        edit_article_id.title = form.title.data
        edit_article_id.body = form.body.data
        db.session.commit()
        return redirect(url_for('edinfo.edinfo'))
    return render_template('add_article.html', title=edit_article_id.title, form=form)


@bp.route('/delete_article/<article_id>')
@login_required
def delete_article(article_id):
    delete_article_id = EdinfoPost.query.filter_by(id=article_id).first()
    db.session.delete(delete_article_id)
    db.session.commit()
    return redirect(url_for('edinfo.edinfo'))
