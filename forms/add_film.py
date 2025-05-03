from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired


class FilmForm(FlaskForm):
    title = StringField('Название фильма', validators=[DataRequired()])
    description = TextAreaField('Описание фильма', validators=[DataRequired()])
    director = StringField('Режисер', validators=[DataRequired()])
    screenwriter = StringField('Сценарист', validators=[DataRequired()])
    duration = StringField('Длительность', validators=[DataRequired()])
    rating = SelectField('Ваша оценка',
                         choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'),
                                  (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')],
                         coerce=int,
                         validators=[DataRequired()])
    premiere = StringField('Премьера', validators=[DataRequired()])
    poster = FileField('Прекрепите постер', validators=[FileRequired()])
    submit = SubmitField('Применить')
