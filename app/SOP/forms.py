from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField
from flask_babel import lazy_gettext as _l

    
class SOPForm(FlaskForm):
    title = StringField(_l('Title'), validators=[DataRequired()])
    body = CKEditorField(_l('SOP'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))
