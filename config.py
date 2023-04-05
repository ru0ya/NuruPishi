#!/usr/bin/python3
"""configuration file"""

import os
from dotenv import load_dotenv
from datetime import timedelta



load_dotenv('cook.env')

class Config:
#     app.secret_key = os.getenv("MY_SECRET_KEY")
     SECRET_KEY =  os.getenv("MY_SECRET_KEY")
     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
     SQLALCHEMY_TRACK_MODIFICATIONS = False
     SESSION_TYPE = 'filesystem'
     PERMANENT_SESSION_LIFETIME = timedelta(days=2)

