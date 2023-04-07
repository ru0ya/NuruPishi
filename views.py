#!/usr/bin/python3
"""routes and templates"""

from flask import Flask, flash, render_template, request, url_for, redirect, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import(
    LoginManager,
    current_user,
    login_required,
    UserMixin,
    login_user,
    logout_user
)
#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
#from flask_session import Session
#from flask_bcrypt import Bcrypt
#from models import User
#from dotenv import load_dotenv
#from datetime import timedelta
#from app_plugins import db, login_manager
#from app_plugins import init_app, db, login_manager
#from forms import register_form, login_form
#from nurupishi import create_app
#from models import Session
from dotenv import load_dotenv
import requests
import os

#app = create_app()
#db.init_app(app)

from app_plugins import login_manager


load_dotenv('cook.env')

views_bp = Blueprint('views_bp', __name__)

#app_id = os.getenv("APP_ID")
#app_key = os.getenv("APP_KEY")


@login_manager.user_loader
def load_user(user_id):
    """returns a User object from user_id"""
    return User.query.get(int(user_id))


@views_bp.route("/")
def index():
    return render_template("base.html")

@views_bp.route("/search", methods=["GET"])
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

@views_bp.route("/signup", methods=["GET", "POST"])
def signup():
    from models import User
    """
    allows a new user to create an account
    using email, username and a password
    """

    form = register_form()

    if form.validate_on_submit():
        try:
            email = form.email.data
            password = form.password.data
            username = form.username.data

            newuser = User(
                username=username,
                email=email,
                password=bcrypt.generate_password_hash(password),
            )

            db.session.add(newuser)
            db.session.commit()
            flash(f"Account Succesfully created", "success")
            return redirect(url_for("login"))
        except Exception as e:
            flash(e, "danger")
     
    return render_template('auth.html', form=form)

@views_bp.route("/login", methods=["GET", "POST"])
def login():
    from models import User
    form = login_form()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()

            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash("Invalid Username or password!", "danger")
        except Exception as e:
            flash(e, "danger")

    return render_template('auth.html', form=form)

@views_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@views_bp.route("/myprofile")
@login_required
def userprofile():
    favorites = current_user.favorites.all()
    bookmarks = current_user.bookmarks.all()

    return render_template("myprofile.html", favorites=favorites, bookmarks=bookmarks)

@views_bp.route("/bookmark", methods=["GET"])
def bookmarks():
    from models import User
    with Session() as session:
        user = session.query(User).filter_by(username=session('username')).first()
        bookmarks = session.query(Bookmarks).filter_by(users_id=user.user_id).all()
        #session.close()

        return render_template('bookmark.html', bookmarks=bookmarks)

@views_bp.route("/favorites", methods=["GET"])
def favorites():
    from models import User
    with Session() as session:
        user = session.query(User).filter_by(username=session('username')).first()
        favorites = session.query(Favorites).filter_by(users_id=user.user_id).all()
        #    session.close()
        return render_templates('favorites.html', favorites=favorites)
