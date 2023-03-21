#!/usr/bin/python3
"""users search history"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


Base = declarative_base()


class SearchHistory(Base):
    __tablename = 'search_history'


    history_id = Column(Integer, primary_key=True)
    users_id = Column(Integer, ForeignKey('user_id.id'), nullable=False)
    query = Column(String(255), nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.now)

    user = relationship('User', backref='search_history')

