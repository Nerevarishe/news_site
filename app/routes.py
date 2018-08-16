from flask import render_template, redirect, url_for
from flask import g
from flask import request
from flask_login import login_required
from flask_babel import _, get_locale
from app import app, db
from app.forms import NewsForm, LawForm
from app.models import News, FaqPost, LawPost


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

@app.before_request
def before_request():
    g.locale = str(get_locale())
