from flask_wtf import Form
from wtforms import TextField, FloatField, DateField
from wtforms.validators import Required


class WeighInForm(Form):
    weight = FloatField('Weight', validators=[Required()])
    date = DateField('Date', validators=[Required()], format='%m/%d/%Y')

