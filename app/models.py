import os
from app import db, app
from flask import url_for
import flask.ext.login as flask_login
from datetime import datetime

class User(db.Model, flask_login.UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=False)
    hash = db.Column(db.String(300), unique=True)

    def __init__(self, email, hash):
        self.email = email
        self.hash = hash
        print(self)


    def __repr__(self):
        return '<User %r %s %r>' % (self.email, self.hash, self.id)
