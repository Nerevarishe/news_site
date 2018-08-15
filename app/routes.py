from flask import render_template, flash, redirect, url_for
from flask import g
from flask import request
from flask_login import current_user, login_user, logout_user, login_required
from flask_babel import _, get_locale
from app import app, db
from app.forms import LoginForm, NewsForm, FaqForm, LawForm
from app.models import User, News, FaqPost, LawPost


#############################################
# News section
###
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
    return render_template('add_news.html', title=_('Add News'), form=form)
    
@app.route('/del_news/<news_id>')
@login_required
def del_news(news_id):
    delete_news_id = News.query.filter_by(id=news_id).first()
    db.session.delete(delete_news_id)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit_news/<news_id>', methods=['GET', 'POST'])
@login_required
def edit_news(news_id):
    edit_news_id = News.query.filter_by(id=news_id).first()
    form = NewsForm(news=edit_news_id.body)
    if form.validate_on_submit():
        edit_news_id.body = form.news.data
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_news.html', form=form)

#############################################
# FAQ section
###
@app.route('/faq', methods=['GET', 'POST'])
def faq():
    faq_posts = FaqPost().query.order_by(FaqPost.timestamp.desc()).all()
    return render_template('faq.html', title=_('FAQ'), faq_posts=faq_posts)

@app.route('/faq/add_faq', methods=['GET', 'POST'])
@login_required
def add_faq():
    form = FaqForm()
    if form.validate_on_submit():
        faq = FaqPost(title=form.title.data, body=form.body.data)
        db.session.add(faq)
        db.session.commit()
        faq_id = faq.id
        return redirect(url_for('faq'))
    return render_template('add_faq.html', title=_('Add FAQ'), form=form)

@app.route('/faq/del_faq/<faq_id>')
@login_required
def del_faq(faq_id):
    delete_faq_id = FaqPost.query.filter_by(id=faq_id).first()
    db.session.delete(delete_faq_id)
    db.session.commit()
    return redirect(url_for('faq'))
    
@app.route('/faq/edit_faq/<faq_id>', methods=['GET', 'POST'])
@login_required
def edit_faq(faq_id):
    edit_faq_id = FaqPost.query.filter_by(id=faq_id).first()
    form = FaqForm(title=edit_faq_id.title, body=edit_faq_id.body)
    if form.validate_on_submit():
        edit_faq_id.title = form.title.data
        edit_faq_id.body = body=form.body.data
        db.session.commit()
        return redirect(url_for('faq'))
    return render_template('add_faq.html', form=form)

#############################################
# Orders section
###    
@app.route('/order', methods=['GET', 'POST'])
def order():
    law_posts = LawPost().query.order_by(LawPost.timestamp.desc()).all()
    return render_template('order.html', title=_('Orders'), law_posts=law_posts)

@app.route('/order/law/<law_id>')
def law(law_id):
    law = LawPost().query.filter_by(id=law_id).first()
    return render_template('law.html', title=law.title, law=law)

@app.route('/order/add_law', methods=['GET', 'POST'])
@login_required
def add_law():
    form = LawForm()
    if form.validate_on_submit():
        law = LawPost(title=form.title.data, body=form.body.data)
        db.session.add(law)
        db.session.commit()
        law_id = law.id
        return redirect(url_for('order'))
    return render_template('add_law.html', title=_('Add law'), form=form)

@app.route('/order/del_law/<law_id>')
@login_required
def del_law(law_id):
    delete_law_id = LawPost.query.filter_by(id=law_id).first()
    db.session.delete(delete_law_id)
    db.session.commit()
    return redirect(url_for('order'))
    
@app.route('/order/edit_law/<law_id>', methods=['GET', 'POST'])
@login_required
def edit_law(law_id):
    edit_law_id = LawPost.query.filter_by(id=law_id).first()
    form = LawForm(title=edit_law_id.title, body=edit_law_id.body)
    if form.validate_on_submit():
        edit_law_id.title = form.title.data
        edit_law_id.body = body=form.body.data
        db.session.commit()
        return redirect(url_for('order'))
    return render_template('add_law.html', form=form)

#############################################
# Login section
###
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
