"""Table User"""

from flask_login import UserMixin
from models.app import db


class User(UserMixin, db.Model):
    """ Model User. plan - film groups watch, watched, dropped.
    vanish - show or hide film list from other users"""
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    login = db.Column(db.String(255), nullable=True, unique=True)
    password = db.Column(db.String(255), nullable=True)
    user_mail = db.Column(db.String(255), nullable=True)
    admin = db.Column(db.Boolean)
    plan = db.relationship("Plan", backref='user', lazy=True)
    comment = db.relationship("Comment", backref='user', lazy=True)
    rating = db.relationship("Rating", backref='user', lazy=True)
    vanish = db.Column(db.Boolean)

    def __init__(self, login, password, user_mail, admin, vanish):
        self.login = login
        self.password = password
        self.user_mail = user_mail
        self.admin = admin
        self.vanish = vanish
