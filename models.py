#!/usr/bin/python3
"""database models"""


from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_session import Session
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import datetime
#from nurupishi import db
#from app_plugins import db
import os


#app = create_app()

#load_dotenv('cook.env')
#Base = declarative_base()

db = SQLAlchemy()

#database_url = os.getenv("DATABASE_URL")
#connection_string = f"mysql://{database_url}"
#engine = create_engine(database_url)

#with app.app_context():
 #   db.create_all()

#from nurupishi import db

class User(UserMixin, db.Model):
    """
    creates user: username, email, password and when
    account was created
    """
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, unique=True)
    creation_date = db.Column(db.Date, nullable=False)

    favorite_recipes = db.relationship('Favorites', backref='user', lazy='dynamic')
    bookmarks = db.relationship('Bookmarks', backref='user', lazy='dynamic')
    search_history = db.relationship('SearchHistory', backref='user', lazy='dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.creation_date = datetime.now()
    
    def __repr__(self):
        return f"<username {self.username}>"

class Favorites(UserMixin, db.Model):
    """
    creates a relationship between user and their favorite recipe
    """
    __tablename__ = 'favorites'
    favorites_id = db.Column(db.Integer, primary_key=True)
    recipe_type = db.Column(db.String(255), nullable=False)
    recipe_id = db.Column(db.Integer, ForeignKey('recipes.recipes_id'), nullable=False)
    users_id = db.Column(db.Integer, ForeignKey('users.user_id'), nullable=False)

class Bookmarks(UserMixin, db.Model):
    """
    saves users bookmarked recipes for future reference
    """
    __tablename__ = 'bookmarks'
    bookmarks_id = db.Column(db.Integer, primary_key=True)
    users_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))

class SearchHistory(UserMixin, db.Model):
    """saves users search history"""
    __tablename__ = 'search_history'
    history_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.user_id'), nullable=False)
    query = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now)

class Recipe(UserMixin, db.Model):
    """saves frequently asked recipes """
    __tablename__ = 'recipes'
    recipes_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.String(1000), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
