#!/usr/bin/python3
"""initializes app"""

from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate


login_manager = LoginManager()
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
