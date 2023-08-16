#!/usr/bin/python3
"""routes and templates"""

from flask import Flask, flash, render_template, request, url_for, redirect, Blueprint, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import(
    LoginManager,
    current_user,
    login_required,
    UserMixin,
    login_user,
    logout_user
)
#from flask_mail import Message
from sqlalchemy.exc import IntegrityError
from slqalchemy.orm import Session
from dotenv import load_dotenv
from datetime import datetime
import requests
import os



from nurupishi.forms import (
        RegistrationForm,
        LoginForm,
        RequestResetForm,
        ResetPasswordForm
        )
from nurupishi.app_plugins import bcrypt
from nurupishi import db
from nurupishi.models import Bookmarks, User, Favorites


load_dotenv('cook.env')

views_bp = Blueprint('views_bp', __name__, template_folder='templates', static_folder='static')


@views_bp.route("/")
def index():
    return render_template("base.html")


@views_bp.route("/search", methods=["GET"])
def search():
    """
    fetches users search query returns recipe
    """
    query = request.args.get('query')
    app_id = current_app.config['APP_ID']
    app_key = current_app.config['APP_KEY']
    url = f'https://api.edamam.com/search?q={query}&app_id={app_id}&app_key={app_key}'
    
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()['hits']
    recipes = []

    for item in data:
        recipe = item['recipe']
        recipes.append(recipe)

    return render_template('search.html', recipes=recipes)


@views_bp.route("/signup", methods=["GET", "POST"])
def signup():
    from nurupishi.models import User
    """
    allows a new user to create an account
    using email, username and a password
    """

    form = RegistrationForm()

    if form.validate_on_submit():
        try:
            email = form.email.data
            password = form.password.data
            username = form.username.data
            creation_date = datetime.utcnow()

            newuser = User(
                username=username,
                email=email,
                password=bcrypt.generate_password_hash(password).decode('utf-8'),
                creation_date=creation_date
            )

            db.session.add(newuser)
            db.session.commit()
            flash(f"Account Succesfully created", "success")
            return redirect(url_for("views_bp.login"))
        except Exception as e:
            flash(e, "danger")
     
    return render_template('auth.html', form=form)


@views_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Validates user for log in
    """
    from nurupishi.models import User
    form = LoginForm()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()

            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('views_bp.index'))
            else:
                flash("Invalid Username or password!", "danger")
        except Exception as e:
            flash(e, "danger")

    return render_template('auth.html', form=form)


@views_bp.route("/logout")
@login_required
def logout():
    """
    Allows logged in user to logout
    """
    logout_user()
    return redirect(url_for('views_bp.login'))


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

        return render_template('bookmark.html', bookmarks=bookmarks)


@views_bp.route("/favorites", methods=["GET"])
def favorites():
    from models import User
    with Session() as session:
        user = session.query(User).filter_by(username=session('username')).first()
        favorites = session.query(Favorites).filter_by(users_id=user.user_id).all()

        return render_template('favorites.html', favorites=favorites)


def send_reset_email(user):
    pass
#    token = user.get_reset_token()
 #   msg = Message('Password Reset Request',
  #                sender='noreply@demo.com',
   #               recipients=[user.email])
   # msg.body = f'''To reset your password, visit the following link:
    #    {url_for('views_bp.reset_token', token=token, external=True)}

       # If you did not make this request then simply ignore this email and
      #  no changes will be made
     #   '''


@views_bp.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    """
    function that allows user to request for
    password reset
    """
    if current_user.is_authenticated:
        return redirect(url_for('views_bp.index'))

    form = RequestResetForm()
    if  form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('views_bp.login'))
    return render_template('reset_request.html', form=form)


@views_bp.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    """
    using the token user recieved, password can
    be successfully reset
    else: invalir token or token expired
    """
    if current_user.is_authenticated:
        return redirect(url_for('views_bp.index'))

    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('views_bp.reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8'),
        user.password = hashed_password
        db.session.commit()   
        flash('Your password has been updated succesfully!', 'success')
        return redirect(url_for('views_bp.login'))
    return render_template('reset_token.html', form=form)



