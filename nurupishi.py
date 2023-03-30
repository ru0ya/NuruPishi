#!/usr/bin/python3
"""
Flask Web App:NuruPishi 
"""

from flask import Flask, flash, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_required
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from flask_session import Session
from models import *
from dotenv import load_dotenv
from datetime import timedelta
import requests
import os


app = Flask(__name__, template_folder="templates")
load_dotenv('cook.env')
app.secret_key = os.getenv("MY_SECRET_KEY") 


"""setting up cookies"""
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=2)

"""creates a login manager"""
login_manager = LoginManager()
login_manager.init_app(app)

app_id = os.getenv("APP_ID")
app_key = os.getenv("APP_KEY")
database_uri = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_DATABASE_URI'] = f'{database_uri}'

db = SQLAlchemy(app)
database_url = os.getenv("DATABASE_URL")
engine = create_engine(database_url)
Session = sessionmaker(bind=engine)
#session = Session()

Base.metadata.create_all(engine)



@login_manager.user_loader
def load_user(user_id):
    """returns a User object from user_id"""

    return User.query.get(int(user_id))



@app.route("/")
def index():
    if current_user.is_authenticated:
        favorites = Favorite.query.filter_by(user_id=current_user.user_id).all()
        bookmarks = Bookmark.query.filter_by(user_id=current_user.user_id).all()
    return render_template("base.html")

@app.route("/search", methods=["GET"])
def search():
    """
    fetches users search query returns recipe
    """
    query = request.args.get('query')
    url = f'https://api.edamam.com/search?q={query}&app_id={app_id}&app_key={app_key}'
#    url = f'https://api.spoonacular.com/recipes/findByIngredients'
#    params = {
 #       'apiKey': app_key,
  #      'ingredients': query,
   #     'number': 9
#    }
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()['hits']
    #data = response.json()
    recipes = []
#   for item in data["results"]:
        #recipe = item['recipe']
#    recipes.append(recipe)
#    print(data)
    for item in data:
        recipe = item['recipe']
        recipes.append(recipe)

    return render_template('search.html', recipes=recipes)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    """
    allows a new user to create an account
    using email, username and a password
    """

#    if current_user.is_authenticated:
 #       return redirect(url_for("index"))

    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not(username and email and password):
            flash("Please provide all required information")
            return redirect(url_for("signup"))

        try:
            user = User(username=username, email=email, password=password, creation_date=datetime.now())
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            existing = db.session.query(User).filter_by(email=email).one()
            flash("Please try again")
        else:
            db.session.commit()
            flash("Succesfully created")
#    session.close()
#    session['user_id'] = user.id
        return redirect(url_for("index"))

    return render_template('signup.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
#        session = Session()
        user = User.query.filter_by(username=request.form['username'].first())
        if user and bcrypt.checkpw(request.form['password'].encode('utf-8'), user.password):
            login_user(user)
            return redirect(url_for("index"))
#            session.close()
 #           session['username'] = user.username
#            return redirect('/')
        else:
  #          session.close()
            flash('Invalid username or password')

    return render_template('login.html')

@app.route("/bookmark", methods=["GET"])
def bookmarks():
    with Session() as session:
        user = session.query(User).filter_by(username=session('username')).first()
        bookmarks = session.query(Bookmarks).filter_by(users_id=user.user_id).all()
        #session.close()
        return render_template('bookmark.html', bookmarks=bookmarks)

@app.route("/favorites", methods=["GET"])
def favorites():
    with Session() as session:
        user = session.query(User).filter_by(username=session('username')).first()
        favorites = session.query(Favorites).filter_by(users_id=user.user_id).all()
    #    session.close()
        return render_templates('favorites.html', favorites=favorites)

if __name__ == "__main__":
    app.run(debug=True)
