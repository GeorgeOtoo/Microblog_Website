'''
instead of putting my configuration in the same place where I create my application I will use a slightly more elaborate structure that allows me to keep my configuration in a separate file. A format that I really like because it is very extensible, is to use a class to store configuration variables.

'''

import os 
basedir = os.path.abspath(os.path.dirname(__file__)) #an absolute path 

class Config(object):

    #The configuration settings are defined as class variables inside the Config class
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    #The Flask-SQLAlchemy extension takes the location of the application's database from the SQLALCHEMY_DATABASE_URI configuration variable
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False