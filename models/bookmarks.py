#!/usr/bin/python3
"""users bookmark"""


from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base()


Base = declarative_base()


class Bookmarks(Base):
    __tablename__ = 'bookmarks'

    bookmarks_id = Column(Integer, primary_key=True)
    users_id = Column(Integer, ForeignKey('user_id.id'), nullable=False)
    name = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False)
    description = Column(String(255))
