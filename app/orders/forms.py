from flask_wtf import FlaskForm
from wtforms import BooleanField ,StringField, SubmitField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField
from flask_babel import lazy_gettext as _l


class LawForm(FlaskForm):
    title = StringField(_l('Title'), validators=[DataRequired()])
    body = CKEditorField(_l('FAQ'), validators=[DataRequired()])
    add_to_news = BooleanField(_l('Add link on news page?'))
    submit = SubmitField(_l('Submit'))
