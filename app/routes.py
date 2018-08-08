from flask import render_template, flash, redirect, url_for
from flask import g
from flask import request
from flask_login import current_user, login_user, logout_user, login_required
from flask_babel import _, get_locale
from app import app, db
from app.forms import LoginForm, NewsForm
from app.models import User, News


@app.route('/', methods=['GET', 'POST'])
@app.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    news = News.query.order_by(News.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=news.next_num) \
        if news.has_next else None
    prev_url = url_for('index', page=news.prev_num) \
        if news.has_prev else None
    return render_template('index.html', title=_('Home'), news=news.items,
                            next_url=next_url, prev_url=prev_url)

@app.route('/add_news', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        news = News(body=form.news.data)
        db.session.add(news)
        db.session.commit()
        news_id = news.id
        return redirect(url_for('index'))
    return render_template('add_news.html', title='Add News', form=form)
    
@app.route('/del_news/<news_id>')
@login_required
def del_news(news_id):
    delete_news_id = News.query.filter_by(id=news_id).first()
    db.session.delete(delete_news_id)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.before_request
def before_request():
    g.locale = str(get_locale())
