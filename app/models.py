from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from app import db


class Event(db.Model):
    __tablename__ = 'event'
    _id = Column(Integer, primary_key=True)
    start = Column(DateTime, unique=False, nullable=False)
    end = Column(DateTime, unique=False, nullable=False)
    author = Column(String(20), unique=False, nullable=False)
    subject = Column(String(80), unique=False, nullable=False)
    description = Column(String(300), unique=False, nullable=True)


class User(db.Model):
    __tablename__ = 'user'

    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)

    def get_id(self):
        return self.email