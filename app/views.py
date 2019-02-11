"""File containing the routes linked to the application."""
from app.tw import TW_Loader
from app import app, login_manager
from app.models import User
from flask import request, redirect, url_for, render_template, jsonify, Blueprint
import flask.ext.login as flask_login
from passlib.hash import sha256_crypt
from app.utils import safe_lower

twl_todo = TW_Loader(app.config['TASKRC'])
tasks = twl_todo.get_tasks()

twl_completed = TW_Loader(app.config['TASKRC'], status="completed")
tasks_completed = twl_completed.get_tasks()
theme = app.config['THEME'].lower()
views = Blueprint('views', __name__,
                  template_folder='themes/{}/templates'.format(theme),
                  static_folder='themes/{}/static'.format(theme),
                  static_url_path='/themes/{}/static'.format(theme))


@login_manager.user_loader
def user_loader(email):
    """Return a user object based on its email.

    :param str email: email of the user we are looking for.
    :return: A user object corresponding to the email.
    :rtype: User
    """
    return User.query.filter_by(email=safe_lower(email)).first()


@login_manager.request_loader
def request_loader(request):
    email = safe_lower(request.form.get('email'))
    user = User.query.filter_by(email=email).first()
    if user is not None:
        if sha256_crypt.verify(request.form['pw'], user.hash):
            flask_login.login_user(user)
    return user

# Login Handling

# FIXME: Each user should have a different taskrc
# @views.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         email = safe_lower(request.form['email'])
#         pw = request.form['pw']
#         hash = sha256_crypt.encrypt(pw)
#         user = User(email, hash)
#         db.session.add(user)
#         db.session.commit()
#         flask_login.login_user(user)
#         return redirect(url_for('index'))
#     elif request.method == 'GET':
#         return render_template('register.html')


@views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = safe_lower(request.form['email'])
        pw = request.form['pw']
        user = User.query.filter_by(email=email).first()
        error_message = ""
        if user is not None:
            if sha256_crypt.verify(pw, user.hash):
                flask_login.login_user(user)
                return redirect(url_for('views.index'))
            else:
                error_message = "Incorrect password."
        else:
            error_message = "User not found."
        return render_template('login.html', title="Signin",
                               error_message=error_message,
                               container_table=True)
    elif request.method == 'GET':
        return render_template('login.html', title="Signin",
                               container_table=True)


@views.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('views.login'))


@views.route('/add', methods=["POST"])
@flask_login.login_required
def add_task():
    twl_todo.add_task(request.form['task'])
    return redirect(url_for('views.index'))


@views.route('/do', methods=['POST', 'PUT'])
@flask_login.login_required
def do_task():
    msg = "ok"
    project = "unassigned"
    if 'id' in request.form:
        task = twl_todo.w.get_task(id=request.form['id'])
        if 'project' in task[1]:
            project = task[1]['project']
        twl_todo.w.task_done(id=request.form['id'])
        twl_todo.refresh_tasks()
        msg = twl_todo.get_tables()
    return jsonify({"error": False, "table": msg, "project": project})


@views.route('/refresh')
@flask_login.login_required
def refresh():
    twl_todo.refresh_tasks()
    twl_completed.refresh_tasks()
    return redirect(url_for('views.index'))


@views.route('/')
@flask_login.login_required
def index(name=None):
    return render_template('index.html', current_user=flask_login.current_user,
                           tasks=twl_todo.get_tables(), title="To Do")


@views.route('/completed')
@flask_login.login_required
def completed(name=None):
    return render_template('completed.html', current_user=flask_login.current_user,
                           tasks=twl_completed.get_tables(), title="Completed")
