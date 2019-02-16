import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    # SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
        
    # Language settings
    LANGUAGES = ['en', 'ru']
    
    # Posts per page on index page
    POSTS_PER_PAGE = 5
    
    # Bootstrap settings
    BOOTSTRAP_SERVE_LOCAL = True
    
    # Upload dir
    UPLOADED_PATH = os.path.join(basedir, 'app/static/uploads')
    
    # CKEditor settings
    CKEDITOR_SERVE_LOCAL = True
    CKEDITOR_FILE_UPLOADER = 'main.upload'
    CKEDITOR_ALLOWEDCONTENT = True
    
    # Flask-Uploads
    UPLOADS_DEFAULT_DEST = UPLOADED_PATH
    UPLOADS_DEFAULT_URL = 'http://localhost:5000/static/uploads/'
 
    UPLOADED_DOCUMENTS_DEST = UPLOADED_PATH
    UPLOADED_DOCUMENTS_URL = 'http://localhost:5000/static/uploads/'
    
    # xlrd settings
    # From what row start to read sheet. Counting from 0.
    FIRST_ROW = 5
    COL_DRUG_NAME = 1
    COL_DATE = 4
    COL_AMOUNT = 3
    # How many rows substract from report bottom
    SUBSTR_ROW = 0
