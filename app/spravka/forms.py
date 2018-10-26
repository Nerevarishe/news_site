from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext as _l

    
class DrugstoreListForm(FlaskForm):
    ds_name = StringField(_l('Drug Store'), validators=[DataRequired()])
    ds_adress = StringField(_l('Adress'), validators=[DataRequired()])
    ds_worktime = StringField(_l('Work Time'), validators=[DataRequired()])
    ds_phone = StringField(_l('Phone'), validators=[DataRequired()])
    ds_ip_phone = StringField(_l('IP Phone'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))


class ServiceCenterListForm(FlaskForm):
    brands = StringField(_l('Brands'), validators=[DataRequired()])
    sc_adress = StringField(_l('Adress'), validators=[DataRequired()])
    sc_phone = StringField(_l('Phone'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))
