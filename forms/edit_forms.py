from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import (FileField, FloatField, IntegerField, StringField,
                     TextAreaField)
from wtforms.validators import DataRequired


class EditFilmForm(FlaskForm):
    title = StringField('Название фильма', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    director = StringField('Режиссер', validators=[DataRequired()])
    screenwriter = StringField('Сценарист', validators=[DataRequired()])
    duration = IntegerField('Длительность (мин)', validators=[DataRequired()])
    rating = FloatField('Рейтинг', validators=[DataRequired()])
    premiere = StringField('Год премьеры', validators=[DataRequired()])
    poster = FileField('Постер', validators=[FileRequired()])