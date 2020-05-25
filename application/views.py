from flask import url_for, render_template, request, flash, g
from flask_login import login_required, current_user

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from application import app, db
from application.songs.models import Song
from application.authors.models import Author
from application.authors import authors

import itertools
import os


@app.before_request
def before_request():
	g.user = current_user

@app.route("/", methods=["GET", "POST"])
def index():

	if request.method == "GET":
		return render_template("index.html")

	if request.method == "POST":

		#----------------------------------------------
		# check if tables are empty
		#----------------------------------------------

		if db.session.query(Author).first() is not None:
			flash("Default authors and songs already exist.", "warning")
			return render_template("index.html")

		#----------------------------------------------
		# add default authors
		#----------------------------------------------

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
		# add default songs
		#----------------------------------------------

		# finnish songs
		for i in range(1,7):
			document_path = os.getcwd()+'/application/static/default_songs/fi/song'+str(i)+'.txt'
			file = open(document_path, 'r', encoding='utf-8')
			title = file.readline().rstrip()
			file.close()
			lyrics = ""
			with open(document_path, encoding='utf-8') as f:
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
			file = open(document_path, 'r', encoding='utf-8')
			title = file.readline().rstrip()
			file.close()
			lyrics = ""
			with open(document_path, encoding='utf-8') as f:
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
				song.authors.extend([Author.query.get(15),Author.query.get(16),Author.query.get(17)])
			elif i == 11:
				song.authors.extend([Author.query.get(18)])
			elif i == 12:
				song.authors.extend([Author.query.get(19)])

			db.session.add(song)
			db.session.commit()

		# french songs
		for i in range(13,19):
			document_path = os.getcwd()+'/application/static/default_songs/fr/song'+str(i)+'.txt'
			file = open(document_path, 'r', encoding='utf-8')
			title = file.readline().rstrip()
			file.close()
			lyrics = ""
			with open(document_path, encoding='utf-8') as f:
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
		try:
			db.session.add(song)
			db.session.commit()
			flash("Default songs added to database.", "success")
		except IntegrityError:
			db.session.rollback()
			flash("Default songs not added to database.", "danger")
		
		return render_template("index.html")
