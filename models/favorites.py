#!/usr/bin/python3
"""a list of users favorite recipes"""


from os import getenv
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Favorites(Base):
    """
    creates a relationship between user and their favorite recipe
    """
    __tablename__ = 'favorites'

    favorites_id = Column(Integer, primary_key=True)
    recipe_type = Column(String)
    recipe_id = Column(Integer, ForeignKey('recipes.id'), nullable=False)
    users_id = Column(Integer, ForeignKey('user_id.id'), nullable=False)


