from app import login, db
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin):
    def get_id(self):
        return "editor"

@login.user_loader
def load_user(id):
    return User()

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author = db.Column(db.String(64))
    tags = db.relationship('Tag', secondary=tags, lazy='subquery',
        backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return '<Post {}>'.format(self.title)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return '<Tag {}>'.format(self.tag)
