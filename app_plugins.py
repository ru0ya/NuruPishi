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

#login_manager.session_protection = "strong"
#login_manager.login_view = "login"
#login_manager.login_message_category = "info"

#def init_app(app):
 #   login_manager.init_app(app)
  #  db.init_app(app)
   # bcrypt.init_app(app)

