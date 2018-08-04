import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LANGUAGES = ['en', 'ru']

    #CKEditor settings
    CKEDITOR_SERVE_LOCAL = True
    CKEDITOR_AUTOGROW_ONSTARTUP = False
    CKEDITOR_FULLPAGE = True
    CKEDITOR_ALLOWEDCONTENT = True
