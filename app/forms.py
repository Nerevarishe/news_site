from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField
from flask_babel import lazy_gettext as _l


class NewsForm(FlaskForm):
    news = CKEditorField(_l('Add news'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))
    
class LawForm(FlaskForm):
    title = StringField(_l('Title'), validators=[DataRequired()])
    body = CKEditorField(_l('FAQ'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))