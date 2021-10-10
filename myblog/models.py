# main/models.py
from datetime import datetime
from myblog import db, login_manager 
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# CONFIGURE USER LOADER #
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

### USER MODEL ###
class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=False, unique=True, index=True)
    username = db.Column(db.String(64), nullable=False, unique=True, index=True)
    description = db.Column(db.String(128), default='Where there is love there is life')
    password_hash = db.Column(db.String(128))
    profile_image = db.Column(db.String(64), nullable=False, default='default_profile.png')
    # Make a relationship to 'posts' table
    posts = db.relationship('Post', back_populates='author', lazy='dynamic')
    # Make a relationship to 'comments' table
    comment = db.relationship('Comment', back_populates='user', lazy='dynamic')

    def __init__(self, email, username, password) -> None:
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def password_check(self, password) -> bool:
        return check_password_hash(self.password_hash, password)

### POST MODEL ###
class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    # Make user's id as foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # Make a relationship to 'users' table
    author = db.relationship('User', back_populates='posts', uselist=False)
    # Make a relationship to 'comments' table
    comment = db.relationship('Comment', back_populates='post', lazy='dynamic')

    def __init__(self, title, content, user_id) -> None:
        self.title = title
        self.content = content
        self.user_id = user_id

# COMMENT MODEL
class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    # Make user's id and post'id as comment table foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    # Make a relationship to 'users' and 'posts' table
    user = db.relationship('User', back_populates='comment', uselist=False)
    post = db.relationship('Post', back_populates='comment', uselist=False)

    def __init__(self, comment, user_id, post_id) -> None:
        self.comment = comment
        self.user_id = user_id
        self.post_id = post_id
