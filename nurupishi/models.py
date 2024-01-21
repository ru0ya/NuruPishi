#!/usr/bin/python3
"""database models"""
from sqlalchemy import(
        Column,
        Integer,
        String,
        Text,
        ForeignKey,
        DateTime,
        Date
        )
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_session import Session
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import URLSafeTimedSerializer as Serializer
from dotenv import load_dotenv
from datetime import datetime
import os


from nurupishi import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    """returns a User object from user_id"""
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    """
    creates user: username, email, password and when
    account was created
    """
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    creation_date = db.Column(db.Date, default=datetime.utcnow)

    favorite_recipes = db.relationship(
            'Favorites',
            backref='user',
            lazy='dynamic'
            )
    bookmarks = db.relationship(
            'Bookmarks',
            backref='user',
            lazy='dynamic'
            )
    search_history = db.relationship(
            'SearchHistory',
            backref='user',
            lazy='dynamic'
            )

    def get_id(self):
        return str(self.user_id)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.user_id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"<username {self.username}>"


class Favorites(UserMixin, db.Model):
    """
    creates a relationship between user and their favorite recipe
    """
    __tablename__ = 'favorites'
    favorites_id = db.Column(db.Integer, primary_key=True)
    recipe_type = db.Column(db.String(255), nullable=False)
    recipe_id = db.Column(
            db.Integer,
            ForeignKey('recipes.recipes_id'),
            nullable=False
            )
    users_id = db.Column(
            db.Integer,
            ForeignKey('users.user_id'),
            nullable=False
            )


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
    user_id = db.Column(
            db.Integer,
            ForeignKey('users.user_id'),
            nullable=False
            )
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
