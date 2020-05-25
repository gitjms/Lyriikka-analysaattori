from flask import Flask
app = Flask(__name__)

import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db_uri = "sqlite:///songs.db"

if os.environ.get("HEROKU"):
	app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
	app.config["ENV"] = 'production'
else:
	app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
	app.config["SQLALCHEMY_ECHO"] = True
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
	app.config["ENV"] = 'development'


db = SQLAlchemy(app)
migrate = Migrate(app, db)

from application import views
from application import models
 
from application.auth import models
from application.auth import views

from application.songs import models
from application.songs import views

from application.authors import models

from application.words import models
from application.words import views


#----------------------------------------------
# login
#----------------------------------------------
from application.auth.models import User
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

app.static_folder = 'static'

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login."

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(user_id)

#----------------------------------------------
# admin and guest accounts
#----------------------------------------------
from sqlalchemy.event import listen
from sqlalchemy import event, DDL

@event.listens_for(User.__table__, 'after_create')
def insert_initial_accounts(*args, **kwargs):
	db.session.add(User(name='admin',username='admin',password='admin', admin=True))
	db.session.add(User(name='guest',username='guest',password='guest', admin=False))
	db.session.commit()


db.create_all()
