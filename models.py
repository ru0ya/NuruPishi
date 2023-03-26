#!/usr/bin/python3
"""database models"""


from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from dotenv import load_dotenv
from datetime import datetime
import os


load_dotenv('cook.env')
Base = declarative_base()

database_url = os.getenv("DATABASE_URL")
#connection_string = f"mysql://{database_url}"
engine = create_engine(database_url)
Base.metadata.create_all(engine)

class Favorites(Base):
    """
    creates a relationship between user and their favorite recipe
    """
    __tablename__ = 'favorites'
    favorites_id = Column(Integer, primary_key=True)
    recipe_type = Column(String)
    recipe_id = Column(Integer, ForeignKey('recipes.id'), nullable=False)
    users_id = Column(Integer, ForeignKey('user_id.id'), nullable=False)

class Bookmarks(Base):
    """
    saves users bookmarked recipes for future reference
    """
    __tablename__ = 'bookmarks'
    bookmarks_id = Column(Integer, primary_key=True)
    users_id = Column(Integer, ForeignKey('user_id.id'), nullable=False)
    name = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False)
    description = Column(String(255))

class User(Base):
    """
    creates user: username, email, password and when
    account was created
    """
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    creation_date = Column(Date, nullable=False)
    
    favorites = relationship('Favorites', backref='user', lazy=True)
    bookmarks = relationship('Bookmarks', backref='user', lazy=True)


class SearchHistory(Base):
    """saves users search history"""
    __tablename__ = 'search_history'
    history_id = Column(Integer, primary_key=True)
    users_id = Column(Integer, ForeignKey('user_id.id'), nullable=False)
    query = Column(String(255), nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.now)
    user = relationship('User', backref='search_history')

class Recipe(Base):
    """saves frequently asked recipes """
    __tablename__ = 'recipes'
    recipes_id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    instructions = Column(String, nullable=False)
    image_url = Column(String, nullable=False)

