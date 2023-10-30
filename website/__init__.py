import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path, environ
import stripe

from flask_login import LoginManager

# Check if running on PythonAnywhere
ON_PYTHONANYWHERE = 'PYTHONANYWHERE_DOMAIN' in os.environ

# Configuration depending on the environment
if ON_PYTHONANYWHERE:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DB_NAME = os.path.join(BASE_DIR, 'instance', 'database.db')
else:
    DB_NAME = "database.db"

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    # Stripe Configuration using environment variables
    app.config['STRIPE_PUBLIC_KEY'] = environ.get('STRIPE_PUBLIC_KEY')
    app.config['STRIPE_SECRET_KEY'] = environ.get('STRIPE_SECRET_KEY')
    stripe.api_key = app.config['STRIPE_SECRET_KEY']

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists(DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

