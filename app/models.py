from sqlalchemy import *
from app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    _id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String)
    authenticated = Column(Boolean, default=False)

    def get_id(self):
        return self._id

    def is_authenticated(self):
        return self.authenticated


class Event(db.Model):
    __tablename__ = 'events'

    _id = Column(Integer, primary_key=True)
    date_start = Column(DateTime, unique=False, nullable=False)
    date_end = Column(DateTime, unique=False, nullable=False)
    author = Column(Integer, ForeignKey('users._id'), nullable=False)
    subject = Column(String(80), unique=False, nullable=False)
    description = Column(String(300), unique=False, nullable=True)

    def get_author(self):
        user = User.query.filter(User._id == self.author).first()
        return user.username
