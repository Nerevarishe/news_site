from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext as _l

    
class DefecturaForm(FlaskForm):
    drug_name = StringField(_l('FAQ'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))
