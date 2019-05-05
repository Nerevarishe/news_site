from flask import render_template, redirect, url_for
from flask_login import login_required
from flask_babel import _
from app import db
# from app.deferred.forms import DeferredForm
# from app.models import DeferredPost
from app.deferred import bp


@bp.route('/', methods=['GET', 'POST'])
def deferred():
    # deferred_posts = DeferredPost().query.order_by(DeferredPost.timestamp.desc()).all()
    return render_template('deferred.html', title=_('deferred'))
