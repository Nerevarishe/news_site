import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    UPLOADED_PATH = os.path.join(basedir, 'uploads')
    
    LANGUAGES = ['en', 'ru']
    
    POSTS_PER_PAGE = 5
    
    #CKEditor settings
    CKEDITOR_SERVE_LOCAL = True
    CKEDITOR_FILE_UPLOADER = 'upload'
    CKEDITOR_ALLOWEDCONTENT = True
