import os
from app.tw import TW_Loader
from app import app, db, login_manager, models
from app.models import User
from flask import Flask, request, redirect, url_for, render_template, g, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
import flask.ext.login as flask_login
from werkzeug import secure_filename
from datetime import datetime
from passlib.hash import sha256_crypt
from flask_table import Table, Col

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

twl = TW_Loader(app.config['TASKRC'])
tasks = twl.get_tasks()


@login_manager.user_loader
def user_loader(email):
    return User.query.filter_by(email=email).first()


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()
    if user is not None:
        hash = sha256_crypt.encrypt(request.form['pw'])
        user.is_authenticated = hash == user.hash
    return user

def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# Login Handling

#@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        pw = request.form['pw']
        hash = sha256_crypt.encrypt(pw)
        user = User(email, hash)
        db.session.add(user)
        db.session.commit()
        flask_login.login_user(user)
        return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        pw = request.form['pw']
        user = User.query.filter_by(email=email).first()
        if user is not None:
            if sha256_crypt.verify(pw, user.hash):
                # flask_login.login_user(user) #call is not working
                flask_login.current_user = user
                flask_login.remember_me = True
                return redirect(url_for('index'))
        return redirect(url_for('login'))
    elif request.method == 'GET':
        return render_template('login.html')

@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('login'))

@app.route('/add', methods=["POST"])
@flask_login.login_required
def add_task():
    twl.add_task(request.form['task'])
    return redirect(url_for('index'))

@app.route('/do', methods=['POST', 'PUT'])
@flask_login.login_required
def do_task():
    msg = "ok"
    project = "unassigned"
    print(request.form)
    if 'id' in request.form:
        task = twl.w.get_task(id=request.form['id'])
        print(task)
        if 'project' in task[1]:
	        project = task[1]['project']
        twl.w.task_done(id=request.form['id'])
        twl.refresh_tasks()
        msg = twl.get_tables()
        print(msg)
    return jsonify({"error":False, "table":msg, "project":project})

@app.route('/refresh')
@flask_login.login_required
def refresh():
    twl.refresh_tasks()
    return redirect(url_for('index'))

@app.route('/')
@flask_login.login_required
def index(name=None):
    return render_template('index.html', current_user=flask_login.current_user, tasks = twl.get_tables())
