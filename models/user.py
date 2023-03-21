#!/usr/bin/python3
"""user data """


from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    """creates user
    Attributes:
        Username
        email
        password
        user_id
        creation_date
        """
        __tablename__ = "users"

        if getenv('NP_TYPE_STORAGE') == 'db':
            user_id = Column(Integer, primary_key=True)
            username = Column(String(50), nullable=False, unique=True)
            email = Column(String(100), nullable=False, unique=True)
            password = Column(String(255), nullable=False)
            creation_date = Column(Date, nullable=False)

            favorites = relationship('Favorite', backref='user', lazy=True)
            bookmarks = relationship('Bookmark', backref='user', lazy=True)
