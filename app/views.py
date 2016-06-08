import os
from app import app, db, login_manager, models
from app.models import User
from flask import Flask, request, redirect, url_for, render_template, g, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
import flask.ext.login as flask_login
from werkzeug import secure_filename
from datetime import datetime
from passlib.hash import sha256_crypt

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

@login_manager.user_loader
def user_loader(id):
     return User.query.get(int(id))


@login_manager.request_loader
def request_loader(request):
    users = models.User.query.all()
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.email = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['pw'] == users[email]['pw']

    return user


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# Login Handling

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        pw = request.form['pw']
        hash = sha256_crypt.encrypt(pw)
        user = models.User(email, hash)
        db.session.add(user)
        db.session.commit()
        print(models.User.query.all())
        flask_login.login_user(user)
        return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form)
        email = request.form['email']
        pw = request.form['pw']
        user = models.User.query.filter_by(email=email).first()
        print(models.User.query.all())
        print(user)
        if user is not None and sha256_crypt.verify(pw, user.hash):
            flask_login.login_user(user)
            return redirect(url_for('index'))
        return redirect(url_for('login'))
    elif request.method == 'GET':
        return render_template('login.html')

@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('login'))


@app.route('/')
# @flask_login.login_required
def index(name=None):
    return render_template('index.html', current_user=flask_login.current_user)
