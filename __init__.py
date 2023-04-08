#!/usr/bin/python3
"""main app"""

import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import db
from app_plugins import bcrypt, login_manager, migrate

load_dotenv('cook.env')


#bcrypt = Bcrypt()
#login_manager = LoginManager()
#migrate = Migrate()

app_id = os.getenv("APP_ID")
app_key = os.getenv("APP_KEY")


login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"


def create_app(app_id, app_key):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.secret_key = os.getenv('MY_SECRET_KEY')
    app_id = os.getenv('APP_ID')
    app_key = os.getenv('APP_KEY')
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SESSION_TYPE'] = 'filesystem'


    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from views import views_bp as views_bp
    app.register_blueprint(views_bp)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    Session = sessionmaker(bind=engine)

    return app

if __name__ == "__main__":
    app = create_app(app_id, app_key)
    app.run()
