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


from nurupishi.app_plugins import bcrypt, login_manager, migrate, db

load_dotenv('cook.env')


def create_app(app_id, app_key):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config['SECRET_KEY'] = os.getenv('MY_SECRET_KEY')
    app.config['APP_ID'] = os.getenv('APP_ID')
    app.config['APP_KEY'] = os.getenv('APP_KEY')
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SESSION_TYPE'] = 'filesystem'



    db.init_app(app)

    login_manager.session_protection = "strong"
    login_manager.login_view = "login"
    login_manager.login_message_category = "info"

    app.config['MAIL_SERVER'] = 'smtp.googlemail.com' 
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
    app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')

    mail.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from .views import views_bp as views_bp
    app.register_blueprint(views_bp)

    with app.app_context():
        db.create_all()

    """engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    Session = sessionmaker(bind=engine)"""

    return app
