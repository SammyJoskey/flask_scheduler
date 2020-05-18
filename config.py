import os

DATABASE_URL = 'postgresql://postgres:081823@localhost:5432/scheduler'


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', DATABASE_URL)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_APP = "app.py"
    SECRET_KEY = os.getenv('SECRET_KEY', 'yoursecretkey12345')
