from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField
from flask_babel import lazy_gettext as _l

    
class DeferredForm(FlaskForm):
    drug_name = StringField(_l('Drug Name'), validators=[DataRequired()])
    drug_amount = StringField(_l('Drug Amount'), validators=[DataRequired()])
    comment = StringField(_l('Comment'))
    submit = SubmitField(_l('Submit'))
