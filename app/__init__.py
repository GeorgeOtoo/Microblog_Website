'''
Here I create and initialize all my extensions
'''

from flask import Flask 
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app) #initializing the database
migrate = Migrate(app, db) #database migrations
login = LoginManager(app) #handles login sessions
login.login_view = 'login' # Flask-Login needs to know what is the view function that handles logins


from app import routes, models, errors #register error handlers