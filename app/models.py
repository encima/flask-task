"""File containing the models linked to the application."""
from app import db
import flask.ext.login as flask_login


class User(db.Model, flask_login.UserMixin):
    """Represent user for the ORM layer."""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=False)
    hash = db.Column(db.String(300), unique=False)

    def __init__(self, email, hash):
        """Instanciate a new user in memory.

        :param str email: email of the user you want to instanciate.
        :param str hash: password hash of the user you want to instanciate.
        """
        self.email = email
        self.hash = hash

    def get_id(self):
        return self.email

    def __repr__(self):
        """Override how represent a user."""
        return '<User %r %s %r>' % (self.email, self.hash, self.id)
