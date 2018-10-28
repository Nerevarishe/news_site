
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField
from flask_babel import lazy_gettext as _l

    
class ChatPanelForm(FlaskForm):
    name = StringField(_l('Username'), validators=[DataRequired()])
    message = StringField(_l('Message'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))
