from flask_wtf import FlaskForm
from wtforms import (BooleanField, EmailField, PasswordField, StringField,
                     SubmitField)
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Введите имя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
