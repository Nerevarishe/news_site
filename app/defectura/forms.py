from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext as _l

    
class DefecturaForm(FlaskForm):
    drug_name = StringField(_l('Defectura'), validators=[DataRequired()])
    comment = StringField(_l('Comment'))
    submit = SubmitField(_l('Submit'))
