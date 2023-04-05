#!/usr/bin/python3
"""
Flask Web App:NuruPishi 
"""

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
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from flask_session import Session
from flask_bcrypt import Bcrypt
#from models import User, Bookmarks, Favorites
import models
from flask_migrate import Migrate
from dotenv import load_dotenv
from datetime import timedelta
#from config import Config
from forms import register_form, login_form
#from app_plugins import init_app, db, login_manager
#from models import Session
#from database import db
from forms import register_form, login_form
import requests
import os


#from app_plugins import init_app

load_dotenv('cook.env')

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()


login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"


#def create_app():
app = Flask(__name__, template_folder="templates")
#app.config.from_object(Config)
#init_app(app)

app.secret_key = os.getenv("MY_SECRET_KEY") 
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=2)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SESSION_TYPE = 'filesystem'

app_id = os.getenv("APP_ID")
app_key = os.getenv("APP_KEY")
database_uri = os.getenv("DATABASE_URL")
#print(database_uri)
#print(os.getenv("DATABASE_URL"))
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

#    from app_plugins import init_app, db
    #login_manager.init_app(app)
    #db.init_app(app)
#    migrate.init_app(app, db)
 #   bcrypt.init_app(app)


db = SQLAlchemy(app)
migrate = Migrate(app, db)
#db.init_app(app)


database_url = os.getenv("DATABASE_URL")
engine = create_engine(database_url)

#(app.config['SQLALCHEMY_DATABASE_URI'])
#    with app.app_context():
 #       from views import views_bp
  
  #app.register_blueprint(views_bp)

#engine = db.engine
Session = sessionmaker(bind=engine)

   # import models
    #import views

#    return app

#app = create_app()
#session = Session()

#Base.metadata.create_all(engine)

#from models import User, Bookmarks, Favorites

@login_manager.user_loader
def load_user(user_id):
    """returns a User object from user_id"""
    return User.query.get(int(user_id))

@app.context_processor
def inject_current_user():
    return dict(current_user=current_user)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["GET"])
def search():
    """
    fetches users search query returns recipe
    """
    query = request.args.get('query')
    url = f'https://api.edamam.com/search?q={query}&app_id={app_id}&app_key={app_key}'
#    url = f'https://api.spoonacular.com/recipes/findByIngredients'
    # params = {
 #       'apiKey': app_key,
  #      'ingredients': query,
   #     'number': 9
#    }
    
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()['hits']
    #data = response.json()
    recipes = []
    for item in data:
        recipe = item['recipe']
        recipes.append(recipe)
#    print(data)
   # for item in data:
    #    recipe = item['recipe']
     #   recipes.append(recipe)

    return render_template('search.html', recipes=recipes)

@app.route("/signup", methods=["GET", "POST"])
def signup():
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
            returnredirect(url_for("login"))
        except Exception as e:
            flash(e, "danger")
    return render_template('auth.html', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
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

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/myprofile")
@login_required
def userprofile():
    favorites = current_user.favorites.all()
    bookmarks = current_user.bookmarks.all()

    return render_template("myprofile.html", favorites=favorites, bookmarks=bookmarks)

@app.route("/bookmark", methods=["GET"])
def bookmarks():
    with Session() as session:
        user = session.query(User).filter_by(username=session('username')).first()
        bookmarks = session.query(Bookmarks).filter_by(users_id=user.user_id).all()
        session.close()
        return render_template('bookmark.html', bookmarks=bookmarks)

@app.route("/favorites", methods=["GET"])
def favorites():
    with Session() as session:
        user = session.query(User).filter_by(username=session('username')).first()
        favorites = session.query(Favorites).filter_by(users_id=user.user_id).all()
        session.close()
        return render_templates('favorites.html', favorites=favorites)

if __name__ == "__main__":
    app.run(debug=True)
