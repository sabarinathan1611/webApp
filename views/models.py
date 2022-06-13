from datetime import date
from email.policy import default
from enum import unique
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    likes= db.relationship('Post_like', backref='like')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(500))
    user_name = db.Column(db.String(150), unique=True)
    admin = db.Column(db.Boolean, default=False)
    gender = db.Column(db.String(150))

    name = db.Column(db.String(150), nullable=True, default='None')
    bio = db.Column(db.Text(150), nullable=True, default='None')
    profile_pic = db.Column(db.String(100000), default='Default/Default.jpeg')

    date = db.Column(db.DateTime(timezone=True), default=func.now())
    notes = db.relationship('Note', backref='poster')
    images = db.relationship('Image', backref='img_poster')
    




class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    img_name = db.Column(db.String(100000), unique=True)
    mimetype = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    likes= db.relationship('Image_like', backref='like')
    

class Post_like(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    post_id =db.Column(db.Integer, db.ForeignKey('note.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime(timezone=True), default=func.now()) 
    
class Image_like(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    post_id =db.Column(db.Integer, db.ForeignKey('image.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime(timezone=True), default=func.now()) 
    