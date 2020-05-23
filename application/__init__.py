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

#----------------------------------------------
# authors
#----------------------------------------------
from application.authors.models import Author
from application.authors import authors

@event.listens_for(Author.__table__, 'after_create')
def insert_initial_authors(*args, **kwargs):
	
	for item in authors.authors_fi:
		song = item[1]
		for auth in item[0]:
			db.session.add(Author(name=auth))
			db.session.commit()

	for item in authors.authors_en:
		song = item[1]
		for auth in item[0]:
			db.session.add(Author(name=auth))
			db.session.commit()
	
	for item in authors.authors_fr:
		song = item[1]
		for auth in item[0]:
			db.session.add(Author(name=auth))
			db.session.commit()

#----------------------------------------------
# 6 default songs per language
#----------------------------------------------
from application.songs.models import Song
import itertools
from application.authors.models import author_song

@event.listens_for(Song.__table__, 'after_create')
def insert_initial_songs(*args, **kwargs):

	# finnish songs
	for i in range(1,7):
		document_path = os.getcwd()+'/application/static/default_songs/fi/song'+str(i)+'.txt'
		file = open(document_path, 'r', encoding='utf8')
		title = file.readline().rstrip()
		file.close()
		lyrics = ""
		with open(document_path) as f:
			for line in itertools.islice(f, 2, None):
				lyrics += line
		language = 'fi'

		song = Song(title,lyrics,language)
		song.account_id = 1

		if i == 1:
			song.authors.extend([Author.query.get(1),Author.query.get(2)])
		elif i == 2:
			song.authors.extend([Author.query.get(3),Author.query.get(4)])
		elif i == 3:
			song.authors.extend([Author.query.get(5),Author.query.get(6)])
		elif i == 4:
			song.authors.extend([Author.query.get(7),Author.query.get(8)])
		elif i == 5:
			song.authors.extend([Author.query.get(9),Author.query.get(10)])
		elif i == 6:
			song.authors.extend([Author.query.get(8),Author.query.get(11)])

		db.session.add(song)
		db.session.commit()

	# english songs
	for i in range(7,13):
		document_path = os.getcwd()+'/application/static/default_songs/en/song'+str(i)+'.txt'
		file = open(document_path, 'r', encoding='utf8')
		title = file.readline().rstrip()
		file.close()
		lyrics = ""
		with open(document_path) as f:
			for line in itertools.islice(f, 2, None):
				lyrics += line
		language = 'en'

		song = Song(title,lyrics,language)
		song.account_id = 1

		if i == 7:
			song.authors.extend([Author.query.get(12)])
		elif i == 8:
			song.authors.extend([Author.query.get(9),Author.query.get(13)])
		elif i == 9:
			song.authors.extend([Author.query.get(14)])
		elif i == 10:
			song.author.extend([Author.query.get(15),Author.query.get(16),Author.query.get(17)])
		elif i == 11:
			song.authors.extend([Author.query.get(18)])
		elif i == 12:
			song.authors.extend([Author.query.get(19)])

		db.session.add(song)
		db.session.commit()

	# french songs
	for i in range(13,19):
		document_path = os.getcwd()+'/application/static/default_songs/fr/song'+str(i)+'.txt'
		file = open(document_path, 'r', encoding='utf8')
		title = file.readline().rstrip()
		file.close()
		lyrics = ""
		with open(document_path) as f:
			for line in itertools.islice(f, 2, None):
				lyrics += line
		language = 'fr'

		song = Song(title,lyrics,language)
		song.account_id = 1

		if i == 13:
			song.authors.extend([Author.query.get(20)])
		elif i == 14:
			song.authors.extend([Author.query.get(21),Author.query.get(22)])
		elif i == 15:
			song.authors.extend([Author.query.get(23),Author.query.get(24)])
		elif i == 16:
			song.authors.extend([Author.query.get(21),Author.query.get(25)])
		elif i == 17:
			song.authors.extend([Author.query.get(26)])
		elif i == 18:
			song.authors.extend([Author.query.get(27)])

		db.session.add(song)
		db.session.commit()

db.create_all()
