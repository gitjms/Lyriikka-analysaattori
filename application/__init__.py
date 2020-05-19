from flask import Flask
app = Flask(__name__)

import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

if os.environ.get("HEROKU"):
	app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
	app.config["ENV"] = 'production'
else:
	app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///songs.db"
	app.config["SQLALCHEMY_ECHO"] = True
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
	app.config["ENV"] = 'development'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from application import views

from application.songs import models
from application.songs import views
 
from application.auth import models
from application.auth import views

#----------------------------------------------
# login
#----------------------------------------------
from application.auth.models import User
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login."

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(user_id)

#----------------------------------------------
# create admin and guest accounts
#----------------------------------------------
from sqlalchemy.event import listen
from sqlalchemy import event, DDL

@event.listens_for(User.__table__, 'after_create')
def insert_initial_accounts(*args, **kwargs):
	db.session.add(User(fullname='admin',username='admin',password='admin', admin=True))
	db.session.add(User(fullname='guest',username='guest',password='guest', admin=False))
	db.session.commit()

#----------------------------------------------
# create 5 default songs
#----------------------------------------------
from application.songs.models import Song

@event.listens_for(Song.__table__, 'after_create')
def insert_initial_songs(*args, **kwargs):
	for i in range(1,6):
		document_path = os.getcwd()+'/application/static/default_songs/song'+str(i)+'.txt'
		file = open(document_path, 'r', encoding='utf8')
		title = file.readline()
		author = file.readline()
		lyrics = file.read()

		song = Song(title,author,lyrics)
		song.account_id = 1
		db.session.add(song)
		db.session.commit()

db.create_all()
