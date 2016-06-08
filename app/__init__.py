import os
from flask import Flask, request, redirect, url_for, render_template, g
from flask_sqlalchemy import SQLAlchemy
import flask.ext.login as flask_login

app = Flask(__name__)
app.config.from_pyfile('sample.cfg', silent=True)
db = SQLAlchemy(app)

login_manager = flask_login.LoginManager()

login_manager.init_app(app)

from app import views, models
