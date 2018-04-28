from flask import render_template, redirect, request, url_for, flash
from app import app, models, db, login_manager, mqtt
from .forms import LoginForm, SignUpForm
from .models import *
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import json
from markupsafe import Markup
import sys
import os
from flask import send_from_directory
from Adafruit_IO import *
import time


# UPLOAD_FOLDER = '/path/to/the/uploads'
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
# photos = UploadSet('photos', IMAGES)

ADAFRUIT_IO_KEY = '80009f64496041f79d5f440181eeb727'
ADAFRUIT_IO_USERNAME = 'caycay'


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    else:
        return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        user = getUserByUsername(username)
        if user is not None:
            return render_template('signup.html', title = "Sign Up", form = form)
        password_hash = generate_password_hash(password)
        newUser = User(username, email, password_hash)
        newUser.addToDatabase()
        login_user(newUser)
        return redirect(url_for('index'))
    return render_template('signup.html', title = "Sign Up", form = form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        comparedUser = getUserByUsername(username)
        if comparedUser is None or not check_password_hash(comparedUser.password_hash, password):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(comparedUser, remember = form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title = 'Log In', form = form)



@app.route('/protected')
@login_required
def protected():
    return 'Logged in as: ' + current_user.username



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))



@app.route('/profile')
def profile():
    mqtt.subscribe("caycay/feeds/meetuser")
    return render_template('dashboard.html')


@app.route('/updateInterests', methods=['POST'])
def updateInterests():
    interests = request.form['int']
    print(interests)
    current_user.updateUserInterests(interests)
    return "great"

@app.route('/getCommonInterests', methods=['GET'])
def getCommonInterests():
    print(findCommonInterests(1,3))
    return "yay"



@app.route('/contacts', methods=['GET'])
@login_required
def showContacts():
    contacts = []
    return render_template("contacts.html", contacts = contacts)


