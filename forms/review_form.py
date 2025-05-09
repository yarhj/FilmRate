from flask_wtf import FlaskForm
from wtforms import (
                     TextAreaField, SelectField, SubmitField)
from wtforms.validators import DataRequired


class ReviewForm(FlaskForm):
    rating = SelectField('Ваша оценка',
                         choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'),
                                  (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')],
                         coerce=int,
                         validators=[DataRequired()])
    review = TextAreaField('Текст', validators=[DataRequired()])
    submit = SubmitField('Опубликовать')