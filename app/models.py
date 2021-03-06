from app import login, db, app
from flask_login import UserMixin
from datetime import datetime
import re

class User(UserMixin):
    def get_id(self):
        return app.config['AUTHOR']

@login.user_loader
def load_user(id):
    return User()

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    blurb = db.Column(db.String(200))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author = db.Column(db.String(64))
    tags = db.relationship('Tag', secondary=tags, lazy='subquery',
        backref=db.backref('posts', lazy=True))
    published = db.Column(db.Boolean)
    slug = db.Column(db.String(300), unique=True, index=True)
    image = db.Column(db.String(310), unique=True)

    def save(self):
        # time added to slug to increase chance of uniqueness
        self.slug = re.sub('[^\w]+', '-', self.title.lower()) + str(datetime.now().strftime("%f"))

    def update_time(self):
        self.timestamp = datetime.utcnow()

    def __repr__(self):
        return '<Post {}>'.format(self.title)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return '<Tag {}>'.format(self.tag)
