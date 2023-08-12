from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150))
    password = db.Column(db.String(150))
    packages = db.relationship('Package', secondary='user_package', back_populates='users', lazy='dynamic')

class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tracking_code = db.Column(db.String(50), nullable=False)
    carrier = db.Column(db.String(50), nullable=False)
    users = db.relationship('User', secondary='user_package', back_populates='packages', lazy='dynamic')

user_package = db.Table('user_package',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('package_id', db.Integer, db.ForeignKey('package.id'), primary_key=True)
)
