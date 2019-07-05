from flask import redirect, url_for
from flask import g, abort
from flask import request
from flask_login import current_user, login_user
from flask_babel import get_locale
from app.main import bp
from app.models import User


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.news'))
    user = User.query.filter_by(username=request.environ.get('HTTP_X_REAL_IP', request.remote_addr)).first()
    if user is None:
        abort(401)
    login_user(user, remember=True)
    return url_for('news.news')


@bp.before_request
def before_request():
    g.locale = str(get_locale())
