import sqlalchemy
from sqlalchemy import ForeignKey
from flask_login import UserMixin
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import relationship


class Films(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'films'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    director = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    average_rating = sqlalchemy.Column(sqlalchemy.Integer)
    poster_path = sqlalchemy.Column(sqlalchemy.String)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, ForeignKey('users.id'))
    author = relationship("User", back_populates="films")