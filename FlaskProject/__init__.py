import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'K\xa5^\x82\x1bV\xa4D\x00_\x8b\xebzv\x05\xa7`\xd5\x08\xbf\xfb\x9a\xbd\xa6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'FlaskProject.db')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.init_app(app)

moment = Moment(app)

import FlaskProject.models
import FlaskProject.views