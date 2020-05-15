from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired

class EventForm(FlaskForm):
    _id = HiddenField('_id')
    author = StringField('author')
    start = DateTimeLocalField('start', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    end = DateTimeLocalField('end', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    subject = StringField('subject', validators=[DataRequired()])
    description = StringField('description')

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])