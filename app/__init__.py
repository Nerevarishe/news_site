from flask import Flask
from flask import request, redirect, url_for
from config import Config
from flask_uploads import UploadSet, DOCUMENTS, configure_uploads
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel
from flask_admin import Admin, AdminIndexView, expose
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
admin = Admin(app, name='News Site')

# Flask-Uploads settings
documents = UploadSet('documents', DOCUMENTS)
configure_uploads(app, documents)

# Flask-Admin Views
from flask_admin.contrib.sqla import ModelView
from app.models import *
class AdminView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth.login', next=request.url))
    
class MyAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        return super(MyAdminIndexView, self).index()
    
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(News, db.session))
admin.add_view(AdminView(FaqPost, db.session))
admin.add_view(AdminView(LawPost, db.session))
admin.add_view(AdminView(ExpdateTable, db.session))
admin.add_view(AdminView(SOPPost, db.session))
admin.add_view(AdminView(EdinfoPost, db.session))

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

from app.defectura import bp as defectura_bp
app.register_blueprint(defectura_bp, url_prefix='/defectura')

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
