from datetime import datetime
from crypt import methods
from turtle import title
from urllib import request
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from app import app, db
from app.forms import EditProfileForm, LoginForm, RegistrationForm, EditProfileForm #import login class
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User





#method to update the user's last seen 
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()



@app.route('/')
@app.route('/index')
@login_required 
def index():
    posts = [
        {
            'author' : {'username' : 'Vania'},
            'body' : 'I got accepted to medical school!'
        },
        {
            'author' : {'username' : 'Winfred'},
            'body' : 'I secured a 100k job!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)

#Another route to handle the login 
@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated: #if user is already logged in
        return redirect(url_for('index'))

    #create and instance of the loginForm 
    form = LoginForm()

    #if statement to check if all validators are true
    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first() #query the database and get username
        if user is None or not user.check_password(form.password.data):#if user doesnt exist or password is wrong
            flash('Invalid Username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data) #log user in
        next_page = request.args.get('next') #next query string argument is obtained
        if not next_page or url_parse(next_page).netloc != '': #if there is no next page
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Login Page', form=form)


#Another route to handle logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


#Route to handle User registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Welcome! You are now a registered User')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


#Route to user profile
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'First Message Testing...'},
        {'author': user, 'body': 'Second Message Testing One Two...'}
    ]

    return render_template('user.html', user=user, posts=posts)


#Route to edit profile
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved! ')
        return redirect(url_for('edit_profile'))
    elif request.method =='GET': #prepopulate the form
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',form=form)