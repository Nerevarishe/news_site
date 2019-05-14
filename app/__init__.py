from flask import Flask
from flask import request, redirect, url_for, current_app
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


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()
ckeditor = CKEditor()
admin = Admin()

# Flask-Uploads settings
documents = UploadSet('documents', DOCUMENTS)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)
    ckeditor.init_app(app)
    admin.init_app(app)

    # Flask-Uploads settings
    configure_uploads(app, documents)

    # Flask-Admin Views
    from flask_admin.contrib.sqla import ModelView
    from app.models import User, News, FaqPost,LawPost,ExpdateTable, SOPPost,EdinfoPost, DefecturaCard

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
    admin.add_view(AdminView(DefecturaCard, db.session))
    admin.add_view(AdminView(DeferredDrug, db.session))

    # Blueprints of modules init
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp, url_prefix='/')

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.faq import bp as faq_bp
    app.register_blueprint(faq_bp, url_prefix='/faq')

    from app.orders import bp as orders_bp
    app.register_blueprint(orders_bp, url_prefix='/orders')

    #from app.expdate import bp as expdate_bp
    #app.register_blueprint(expdate_bp, url_prefix='/expdate')

    from app.SOP import bp as SOP_bp
    app.register_blueprint(SOP_bp, url_prefix='/SOP')

    from app.edinfo import bp as edinfo_bp
    app.register_blueprint(edinfo_bp, url_prefix='/edinfo')

    from app.defectura import bp as defectura_bp
    app.register_blueprint(defectura_bp, url_prefix='/defectura')

    from app.spravka import bp as spravka_bp
    app.register_blueprint(spravka_bp, url_prefix='/spravka')

    from app.chat import bp as chat_bp
    app.register_blueprint(chat_bp, url_prefix='/chat')

    from app.schedule import bp as schedule_bp
    app.register_blueprint(schedule_bp, url_prefix='/schedule')

    from app.deferred import bp as deferred_bp
    app.register_blueprint(deferred_bp, url_prefix='/deferred')

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

        return app


# Babel module init
@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])


from app import models
