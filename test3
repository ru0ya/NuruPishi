#!/usr/bin/python3
"""database models"""


from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


load_dotenv('cook.env')
Base = declarative_base()
os.environ['NP_TYPE_STORAGE'] = 'db'

database_url = os.getenv("DATABASE_URL")
connection_string = f"mysql://{database_url}"
engine = create_engine(connection_string)
Base.metadata.create_all(engine)

class Favorites(Base):
    """
    creates a relationship between user and their favorite recipe
    """
    __tablename__ = 'favorites'
    if getenv('NP_STORAGE_TYPE') == 'db':
        favorites_id = Column(Integer, primary_key=True)
        recipe_type = Column(String)
        recipe_id = Column(Integer, ForeignKey('recipes.id'), nullable=False)
        users_id = Column(Integer, ForeignKey('user_id.id'), nullable=False)

class Bookmarks(Base):
    __tablename__ = 'bookmarks'
    if getenv('NP_STORAGE_TYPE') == 'db':
        bookmarks_id = Column(Integer, primary_key=True)
        users_id = Column(Integer, ForeignKey('user_id.id'), nullable=False)
        name = Column(String(255), nullable=False)
        url = Column(String(255), nullable=False)
        description = Column(String(255))

class User(Base):
    """creates user"""
    __tablename__ = "users"
    
    if getenv('NP_TYPE_STORAGE') == 'db':
        user_id = Column(Integer, primary_key=True)
        username = Column(String(50), nullable=False, unique=True)
        email = Column(String(100), nullable=False, unique=True)
        password = Column(String(255), nullable=False)
        creation_date = Column(Date, nullable=False)

        favorites = relationship('Favorite', backref='user', lazy=True)
        bookmarks = relationship('Bookmark', backref='user', lazy=True)


class SearchHistory(Base):
    __tablename = 'search_history'

    if getenv('NP_TYPE_STORAGE') == 'db':
        history_id = Column(Integer, primary_key=True)
        users_id = Column(Integer, ForeignKey('user_id.id'), nullable=False)
        query = Column(String(255), nullable=False)
        timestamp = Column(DateTime, nullable=False, default=datetime.now)
        user = relationship('User', backref='search_history')

class Recipe(Base):
    """ """
    def __init__(self, title, description, image_url):
        self.title = title
        self.description = description
        self.image_url = image_url

        __tablename__ = 'recipes'

        if getenv('NP_TYPE_SRORAGE') == 'db':
            recipes_id = Column(Integer, primary_key=True)
            title = Column(String(100), nullable=False)
            description = Column(Text, nullable=False)
            instructions = Column(String, nullable=False)
            image_url = Column(String, nullable=False)

