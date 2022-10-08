'''
Here I create and initialize all my extensions
'''
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
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


# to get emails to send out on errors, add a SMTPHandler instance to the Flask logger object which is app.logger
if not app.debug:
    # the email server exists in the configuration.
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

#the code above creates a SMTPHandler instance, sets its level so that it only reports errors and not warnings, informational or debugging messages, and finally attaches it to the app.logger object from Flask.


#I'm also going to maintain a log file for the application
# To enable a file based log another handler, this time of type RotatingFileHandler, needs to be attached to the application logger

    if not os.path.exists('logs'):
        os.mkdir('logs')
    #I'm writing the log file with name microblog.log in a logs directory, which I create if it doesn't already exist.
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,backupCount=10) 
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')

#The RotatingFileHandler class is nice because it rotates the logs, ensuring that the log files do not grow too large when the application runs for a long time. In this case I'm limiting the size of the log file to 10KB, and I'm keeping the last ten log files as backup.

#The logging.Formatter class provides custom formatting for the log messages. Since these messages are going to a file, I want them to have as much information as possible. So I'm using a format that includes the timestamp, the logging level, the message and the source file and line number from where the log entry originated.

#To make the logging more useful, I'm also lowering the logging level to the INFO category, both in the application logger and the file logger handler. logging categories: they are DEBUG, INFO, WARNING, ERROR and CRITICAL in increasing order of severity.

from app import routes, models, errors #register error handlers