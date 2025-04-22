from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired()])
    username = StringField('Введите имя', validators=[DataRequired()])
    email = EmailField('Введите почту', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')
