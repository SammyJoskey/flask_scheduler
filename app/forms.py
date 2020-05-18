from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.html5 import EmailField, DateTimeField
from wtforms.validators import InputRequired, DataRequired, Email, EqualTo
import datetime

class CreateUserForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[InputRequired(), DataRequired()])
    email = EmailField('Электронная почта', validators=[InputRequired(), DataRequired(), Email()])
    password = PasswordField("Введите пароль", validators=[InputRequired(), DataRequired()])

    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = EmailField('Электронная почта', validators=[InputRequired(), DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[InputRequired(), DataRequired()])

    submit = SubmitField('Войти')


class EventForm(FlaskForm):
    date_start = DateTimeField("Начало", default=datetime.datetime.now(), format='%Y-%m-%d %H:%M:%S',
                               validators=[DataRequired(message="Неправильный формат даты")], )
    date_end = DateTimeField("Окончание", default=datetime.date.today(), format='%Y-%m-%d %H:%M:%S',
                             validators=[DataRequired(message="Неправильный формат даты")], )
    subject = StringField("Тема", validators=[InputRequired(), DataRequired()])
    description = StringField("Описание", validators=[DataRequired()])

    submit = SubmitField('Сохранить')
