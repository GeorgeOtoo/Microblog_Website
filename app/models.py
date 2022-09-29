'''
The data that will be stored in the database will be represented by a collection of classes, usually called database models.

The User class created above inherits from db.Model, a base class for all models from Flask-SQLAlchemy. This class defines several fields as class variables. Fields are created as instances of the db.Column class, which takes the field type as an argument, plus other optional arguments that, for example, allow me to indicate which fields are unique and indexed, which is important so that database searches are efficient.

The __repr__ method tells Python how to print objects of this class, which is going to be useful for debugging.
'''

from datetime import datetime #import date package
from werkzeug.security import generate_password_hash, check_password_hash # import packages to create password hash and check it
from app import db, login #import db, login from application
from flask_login import UserMixin #checks state of the login
from hashlib import md5

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    
    # converts user password to a password hash
    def set_password(self, password): 
        self.password_hash = generate_password_hash(password)

    #verifies password hash to the password given
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    #Creating gravatar images to profile(returns URL of the user's avatar image)
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=wavatar&s={}'.format(
            digest, size)

@login.user_loader
def load_user(id):
    '''
    Because Flask-Login knows nothing about databases, it needs the application's help in loading a user. For that reason, the extension expects that the application will configure a user loader function, that can be called to load a user given the ID
    '''
    return User.query.get(int(id))




'''
The posts table will have the required id, the body of the post and a timestamp. But in addition to these expected fields, I'm adding a user_id field, which links the post to its author. You've seen that all users have a id primary key, which is unique. The way to link a blog post to the user that authored it is to add a reference to the user's id, and that is exactly what the user_id field is. This user_id field is called a foreign key.

The first argument to db.relationship is the model class that represents the "many" side of the relationship. This argument can be provided as a string with the class name if the model is defined later in the module. The backref argument defines the name of a field that will be added to the objects of the "many" class that points back at the "one" object. 
'''
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
