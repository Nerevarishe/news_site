from flask import Flask
from flask import request
from config import Config
from flask_uploads import UploadSet, DOCUMENTS, configure_uploads
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel
import logging
from logging.handlers import RotatingFileHandler
import os


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
babel = Babel(app)
ckeditor = CKEditor(app)

# Flask-Uploads settings
documents = UploadSet('documents', DOCUMENTS)
configure_uploads(app, documents)


# Blueprints of modules init
from app.errors import bp as errors_bp
app.register_blueprint(errors_bp)

from app.auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')

from app.faq import bp as faq_bp
app.register_blueprint(faq_bp, url_prefix='/faq')

from app.orders import bp as orders_bp
app.register_blueprint(orders_bp, url_prefix='/orders')

from app.expdate import bp as expdate_bp
app.register_blueprint(expdate_bp, url_prefix='/expdate')

from app.SOP import bp as SOP_bp
app.register_blueprint(SOP_bp, url_prefix='/SOP')

from app.edinfo import bp as edinfo_bp
app.register_blueprint(edinfo_bp, url_prefix='/edinfo')


# Babel module init
@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])

if not app.debug:
    # E-mail configuration

    # Log File configuration
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/newssite.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('News site startup')

from app import routes, models
