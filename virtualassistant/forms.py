from flask_wtf import FlaskForm
from wtforms import StringField, FileField, ValidationError
from wtforms.validators import DataRequired


def alpha_val(form, field):
    if not field.data.isalpha():
        raise ValidationError("Please use only letters")

class CreateForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), alpha_val])
    surname = StringField('surname', validators=[DataRequired(), alpha_val])
    job = StringField('job', validators=[DataRequired()])
    photo = FileField()

class UpdateForm(FlaskForm):
    name = StringField('name', validators=[alpha_val])
    surname = StringField('surname', validators=[alpha_val])
    job = StringField('job')
    photo = FileField()