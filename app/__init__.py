"""Application initialization."""
import os
import flask.ext.login as flask_login

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
if os.path.exists("app/config/local.cfg"):
    app.config.from_pyfile('config/local.cfg', silent=True)
else:
    app.config.from_pyfile('sample.cfg', silent=True)

db = SQLAlchemy(app)

login_manager = flask_login.LoginManager()
from app.views import views  # noqa
app.register_blueprint(views)
login_manager.login_view = "views.login"

login_manager.init_app(app)

from app import models  # noqa
