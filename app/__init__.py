from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

Bootstrap(app)

from app import routes, models
