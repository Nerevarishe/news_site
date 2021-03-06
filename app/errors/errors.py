from flask import render_template
from app import db
from app.errors import bp


@bp.app_errorhandler(401)
def forbidden_error(error):
    return render_template('401.html'), 401


@bp.app_errorhandler(403)
def forbidden_error(error):
    return render_template('403.html'), 403


@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
