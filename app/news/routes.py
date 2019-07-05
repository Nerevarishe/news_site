import os
from flask import render_template, redirect, url_for, send_from_directory, current_app
from flask import request
from flask_login import login_required
from flask_ckeditor import upload_fail, upload_success
from app import db
from app.main import bp
from app.news.forms import NewsForm
from app.models import News


@bp.route('/', methods=['GET', 'POST'])
def news():
    page = request.args.get('page', 1, type=int)
    news_list = News.query.order_by(News.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('news.news', page=news.next_num) \
        if news.has_next else None
    prev_url = url_for('news.news', page=news.prev_num) \
        if news.has_prev else None
    return render_template('news.html', title=_('Home'), news=news_list.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/add_news', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        news = News(body=form.news.data)
        db.session.add(news)
        db.session.commit()
        return redirect(url_for('news.news'))
    return render_template('add_news.html', title=_('Add News'), form=form)


@bp.route('/files/<filename>')
def uploaded_files(filename):
    path = current_app.config['UPLOADED_PATH']
    return send_from_directory(path, filename)


@bp.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')
    extension = f.filename.split('.')[1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    f.save(os.path.join(current_app.config['UPLOADED_PATH'], f.filename))
    url = url_for('main.uploaded_files', filename=f.filename)
    return upload_success(url=url)


@bp.route('/del_news/<news_id>')
@login_required
def del_news(news_id):
    delete_news_id = News.query.filter_by(id=news_id).first()
    db.session.delete(delete_news_id)
    db.session.commit()
    return redirect(url_for('news.news'))


@bp.route('/edit_news/<news_id>', methods=['GET', 'POST'])
@login_required
def edit_news(news_id):
    edit_news_id = News.query.filter_by(id=news_id).first()
    form = NewsForm(news=edit_news_id.body)
    if form.validate_on_submit():
        edit_news_id.body = form.news.data
        db.session.commit()
        return redirect(url_for('news.news'))
    return render_template('add_news.html', form=form)
