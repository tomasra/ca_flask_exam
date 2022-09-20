from flask_login import UserMixin
from expenses_app import app, db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), unique=True, nullable=False)
    groups = db.relationship('Group', secondary='users_groups', back_populates='users')
    expenses = db.relationship('Expense', back_populates='user')


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    expenses = db.relationship('Expense', back_populates='group')
    users = db.relationship('User', secondary='users_groups', back_populates='groups')


class Expense(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    group = db.relationship('Group', back_populates='expenses')
    user = db.relationship('User', back_populates='expenses')


users_groups = db.Table('users_groups', db.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'), primary_key=True)
)
