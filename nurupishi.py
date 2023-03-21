#!/usr/bin/python3
"""
Flask Web App:NuruPishi 
"""

from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_required
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *
from dotenv import load_dotenv
import requests
import os


app = Flask(__name__, template_folder="templates")

load_dotenv('cook.env')

"""creates a login manager"""
login_manager = LoginManager()
login_manager.init_app(app)

app_id = os.getenv("APP_ID")
app_key = os.getenv("APP_KEY")


def load_user(user_id):
    """returns a User object from user_id"""
    return User.query.get(int(user_id))


@app.route("/")
def index():
    if current_user.is_authenticated:
        favorites = Favorite.query.filter_by(user_id=current_user.user_id).all()
        bookmarks = Bookmark.query.filter_by(user_id=current_user.user_id).all()
    return redirect(url_for("search"))
@app.route("/search", methods=["GET"])
def search():
    """
    fetches users search query returns recipe
    """
    query = request.args.get('query')
    url = f'https://api.edamam.com/search?q={query}&app_id={app_id}&app_key={app_key}'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()['hits']
    recipes = []
    for item in data:
        recipe = item['recipe']
        recipes.append(recipe)

    return render_template('search.html', recipes=recipes)

@app.route("/signup", methods=["POST"])
def signup():
    pass
#    session = Session()
   # user = User(username=request.form['username'], email=request.form['email'], password=request.form['password'], creation_date=datetime.now())
  #  session.add(user)
 #   session.commit()
#    session.close()


@app.route("/login", methods=["GET"])
def login():
    if request.method == "POST":
        session = Session()
        user = session.query(User).filter_by(username=request.form['username'], password=request.form['password']).first()
        if user:
            session.close()
            return redirect('/home')
        else:
            session.close()
            flash('Invalid username or password')

    return render_template('login.html')

@app.route("/bookmark", methods=["GET"])
def bookmarks():
    session = Session()
    user = session.query(User).filter_by(username=session['username']).first()
    bookmarks = user.bookmarks
    session.close()
    return render_template('bookmark.html', bookmarks=bookmarks)

@app.route("/favorites", methods=["GET"])
def favorites():
    session = Session()
    user = session.query(User).filter_by(username=session['username']).first()
    favorites = user.favorites
    session.close()
    return render_templates('favorites.html', favorites=favorites)

if __name__ == "__main__":
    app.run(debug=True)
