from flask import render_template, flash, redirect, url_for
from flask import g
from flask_login import current_user, login_user, logout_user, login_required
from flask_babel import _, get_locale
from app import app, db
from app.forms import LoginForm, NewsForm
from app.models import User, News


@app.route('/')
@app.route('/index')
def index():
    news = News.query.order_by(News.timestamp.desc()).all()
    return render_template('index.html', title=_('Home'), news=news)


@app.route('/schedule')
def schedule():
    return render_template('schedule.html', title=_('Schedule'))


@app.route('/employees')
def employees():
    return render_template('employees.html', title=_('Employees'))


@app.route('/about')
def about():
    return render_template('about.html', title=_('About'))


@app.route('/science')
def science():
    return render_template('science.html', title=_('Science'))

@app.route('/add_news', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        news = News(body=form.news.data)
        db.session.add(news)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_news.html', title='Add News', form=form)

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