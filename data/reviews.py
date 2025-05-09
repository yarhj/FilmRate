import sqlalchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class Reviews(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'reviews'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    review = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    review_rating = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, ForeignKey('users.id'))
    film_id = sqlalchemy.Column(sqlalchemy.Integer, ForeignKey('films.id'))
    user = relationship("User", back_populates="review")
    film = relationship("Films", back_populates="review")