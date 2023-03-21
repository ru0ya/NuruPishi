#!/usr/bin/python3
"""
This is the recipe class
Saves frequently asked queries to
reduce number of requests to the API
"""

from os import getenv
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Recipe(Base):
    """ """
    def __init__(self, title, description, image_url):
        self.title = title
        self.description = description
        self.image_url = image_url

    if getenv('NP_TYPE_SRORAGE') == 'db':
        __tablename__ = 'recipes'

        recipes_id = Column(Integer, primary_key=True)
        title = Column(String(100), nullable=False)
        description = Column(Text, nullable=False)
        instructions = Column(String, nullable=False)
        image_url = Column(String, nullable=False)
