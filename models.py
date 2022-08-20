from flask_login import UserMixin

from main import my_db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Text, Table, ForeignKey, Column, Boolean


class Users(my_db.Model , UserMixin):
    __tablename__='users'
    id = my_db.Column(Integer, primary_key=True)
    username = my_db.Column(String(80), nullable=False)
    email = my_db.Column(String(120), unique=True, nullable=False)
    password=my_db.Column(String(500), nullable=False)


class Words(my_db.Model, UserMixin):
    __tablename__='words'
    id=my_db.Column(Integer, primary_key=True)
    word=my_db.Column(String)
    # definitions=my_db.Column(String)
    # examples=my_db.Column(String)
    # saved=my_db.Column(String)


class Saved(my_db.Model, UserMixin):
    __tablename__='saved'
    id=my_db.Column(Integer, primary_key=True)
    word=my_db.Column(String)


# my_db.drop_all()
# my_db.create_all()
