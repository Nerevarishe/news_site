from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField
from flask_babel import lazy_gettext as _l


class NewsForm(FlaskForm):
    news = CKEditorField(_l('Add news'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))
