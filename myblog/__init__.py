# main/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

### INIT FLASK APP ###
app = Flask(__name__)

### CONFIGURE SECRET KEY FOR FLASKFORM ###
app.config['SECRET_KEY'] = 'my_key'

### CONFIGURE SQLACHEMY DATABASE ###
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

### CONFIGURE MIGRATE ###
Migrate(app, db)

### CONFIGURE LOGIN MANAGER ###
login_manager = LoginManager()
# We can now pass in our app to the login manager
login_manager.init_app(app)
# Tell users what view to go to when they need to login.
login_manager.login_view = 'users.login'

### REGISTER BLUEPRINT ###
from myblog.core.views import core_blueprint
from myblog.users.views import users_blueprint
from myblog.posts.views import posts_blueprint
from myblog.errors.errors_handler import errors_page

app.register_blueprint(core_blueprint)
app.register_blueprint(users_blueprint)
app.register_blueprint(posts_blueprint)
app.register_blueprint(errors_page)