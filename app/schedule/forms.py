from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext as _l


# Employee add/edit form
class AddEmployee(FlaskForm):
    last_name = StringField(_l('Last Name:'), validators=[DataRequired()])
    first_name = StringField(_l('First Name:'), validators=[DataRequired()])
    patronymic = StringField(_l('Patronymic:'), validators=[DataRequired()])
    is_active = BooleanField(_l('Activate Employee?'), default='checked')
    preferred_time = SelectField(_l('Preferred time:'), choices=[('', _l('None')), ('7:30', '7:30'), ('8:30', '8:30'),
                                                                 ('9:00', '9:00'), ('10:00', '10:00')])
    work_hours_in_day = SelectField(_l('Work hours in day:'), choices=[('9', '9'), ('12.5', '12.5')])
    submit = SubmitField(_l('Submit'))
