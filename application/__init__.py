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
 
from application.auth import models
from application.auth import views

from application.songs import models
from application.songs import views

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
# admin and guest accounts
#----------------------------------------------
from sqlalchemy.event import listen
from sqlalchemy import event, DDL

@event.listens_for(User.__table__, 'after_create')
def insert_initial_accounts(*args, **kwargs):
	db.session.add(User(fullname='admin',username='admin',password='admin', admin=True))
	db.session.add(User(fullname='guest',username='guest',password='guest', admin=False))
	db.session.commit()

#----------------------------------------------
# 5 default songs
#----------------------------------------------
from application.songs.models import Song

@event.listens_for(Song.__table__, 'after_create')
def insert_initial_songs(*args, **kwargs):
	def song_1():
		title = "Armo Jumalan"
		author = "Jens Nicolai Ludvig Schjörring, H. S. Thompson"
		lyrics = "Armo Jumalan\nlailla kirkkahan\nlähteen puuhtaan\nkuohuilee.\n\nSyvyydessä sen\narmolähtehen\nelon helmi\nhohtelee.\n\nArmo Jumalan\nlevon suloisan\nsydämehen\naina suo.\nJeesus-nimessä\nonnen löydät sä.\nTaivahan se\nmyötään tuo."
	 
		return title, author, lyrics

	def song_2():
		title = "Ah, saavu, Jeesus"
		author = "Abraham Achrenius, Toisinto Ylistarosta"
		lyrics = "Ah, saavu, Jeesus,\nkeskellemme,\nniin sydämemme rukoilee.\nJo joutuu\nehtoo matkallemme,\njo armon päivä alenee.\nYö kohta peittää\nmaailman,\ntaisteluun käymme\nkuoleman.\n\nAh, kulje, Jeesus,\nrinnallamme,\nniin rakastamme,\nuskomme.\nSuo rohkeutta\nsodassamme,\nSinussa lepää toivomme.\nKun Jeesus\nseurassamme on,\non yökin päivä verraton.\n\nVain siitä syttyy\nsydämemme,\nkun saavut, Jeesus,\nkallehin,\nkirkastat armon\nriemuksemme,\ntaas vaikka\nkasvos salaatkin.\nTuntea saimme Jeesuksen,\nja ilo täyttää sydämen.\n\nIloiten sitten\nkiiruhdamme\nrientämään\nystäväimme luo\nja siellä\nheille julistamme:\nVieläkin avun Herra suo!\nMe luulimme,\non kuollut Hän,\nvaan näimme\nHänen elävän."
	 
		return title, author, lyrics

	def song_3():
		title = "Ah, tulla jo Sun valtakuntasi suo"
		author = "Lina Sandell-Berg, Gunr Wennerberg"
		lyrics = "Ah, tulla jo Sun\nvaltakuntasi suo,\nja voimasi,\nHerra, Sä näytä.\nVie armosi viestiä\nkansojen luo\nja lähettis\ntulella täytä.\n|: Maan äärten suo\nkutsusi kuulla.:|\n\nSä siunaa ja\nvahvista palvelijas,\nmi kaukana\nlippua kantaa.\nSuo tuntea heidän\nSun rakkauttas\nja rauhaa,\nmi lohtua antaa,\n|: kun vaarojen\nteillä he käyvät.:|\n\nSuo voimasi heille\nSä taistelussaan\nja uskoa,\nuskollisuutta,\nniin että he toivossa\nkylvävät vaan\nja vartoovat\naikaasi uutta,\n|: kun korjata\nsadon Sä annat.:|\n\nJos kylvön he\nverellä kastella saa,\nniin armoa vain\non se Herran.\nNäin siunausta kasvaa\nvoi kuivakin maa,\nmi sadon myös\nkantavi kerran,\n|: ja tappio\nvoitoksi vaihtuu.:|"
	 
		return title, author, lyrics

	def song_4():
		title = "Ah, etten mitään oisi"
		author = "Georgiana M. Taylor, Tuntematon"
		lyrics = "Ah, etten mitään oisi,\ntyhjä, murrettu astia vaan,\npantu Mestarin\njalkain juureen\nkorjaustansa vartoamaan -\ntyhjä, Hän että voi täyttää,\nkun työtänsä\nkäyn tekemään,\nniin murrettu,\nettä voi käyttää\nmua syntistä etsimään.\n\nAh, etten mitään oisi,\nyksin Herraani tottelisin,\novenvartijan lailla valppaan\nHänen käskynsä täyttelisin -\nkanteleen\nsointuna helkkäin,\nkun Taitajan tahto on niin,\ntai vaieten,\nkunnes mun jälleen\nsaa sointuihin taivaisiin."
	 
		return title, author, lyrics

	def song_5():
		title = "Ajan myrskyaallot"
		author = "Johnson Jr. Oatman, Edwin O. Excell"
		lyrics = "Ajan myrskyaallot\nkun sua heittävät,\nsynkät pilvet usein\ntaivaan peittävät,\nmuista, että Jeesus\nmyrskyn hiljentää,\nepäuskon pilvetkin\nvoi hälventää.\n\n  Laske siunaukset\n  yksittäin,\n  huomaa Herran\n  hyvyys päivittäin.\n  Muista työnsä\n  suuret, valtavat,\n  uutta intoa ne\n  sulle antavat.\n\nPäivän helle matkalla\nkun ahdistaa,\nristi raskas painaa,\nHerra vahvistaa.\nSiunaukset\nkestävyyttä sulle tuo,\nPyhä Henki aina\nuutta voimaa suo.\n\nKun sä katsot\nrikkautta maailman,\nmuista: Jeesus antaa\naarteen suurimman.\nAnsaita ei kukaan\nsitä koskaan voi,\nlahjana sen\ntaivahasta Jeesus toi."
	 
		return title, author, lyrics

	title = song_1()[0]
	author = song_1()[1]
	lyrics = song_1()[2]
	song1 = Song(title,author,lyrics)
	song1.account_id = 1
	db.session.add(song1)
	db.session.commit()

	title = song_2()[0]
	author = song_2()[1]
	lyrics = song_2()[2]
	song2 = Song(title,author,lyrics)
	song2.account_id = 1
	db.session.add(song2)
	db.session.commit()

	title = song_3()[0]
	author = song_3()[1]
	lyrics = song_3()[2]
	song3 = Song(title,author,lyrics)
	song3.account_id = 1
	db.session.add(song3)
	db.session.commit()

	title = song_4()[0]
	author = song_4()[1]
	lyrics = song_4()[2]
	song4 = Song(title,author,lyrics)
	song4.account_id = 1
	db.session.add(song4)
	db.session.commit()

	title = song_5()[0]
	author = song_5()[1]
	lyrics = song_5()[2]
	song5 = Song(title,author,lyrics)
	song5.account_id = 1
	db.session.add(song5)
	db.session.commit()

db.create_all()
