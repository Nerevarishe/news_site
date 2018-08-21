
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext as _l

    
class ExpdateAddItemForm(FlaskForm):
    drug_name = StringField(_l('Drug name'), validators=[DataRequired()])
    exp_date = DateField(_l('Exp. Date'), format='%d/%m/%Y', validators=[DataRequired()])
    amount = StringField(_l('Amount'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))
