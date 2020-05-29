# -*- coding: UTF-8 -*-
from flask import redirect, url_for, render_template, request, flash, g
from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired
from flask_login import login_required, current_user

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.sql import text
from sqlalchemy import func, distinct, asc

from application import app, db
from application.songs.models import Song
from application.auth.models import User
from application.words.models import Words
from application.authors.models import Author, author_song
from application.songs.forms import SongForm

# Lomakkeen näyttämisen ja lähetyksen vastaanottava toiminnallisuus.

@app.before_request
def before_request():
	g.user = current_user


#-----------------------------------------
#		INDEX: songs_index()
#-----------------------------------------
@app.route("/")
def songs_index():
	return render_template("index.html")


#-----------------------------------------
#		MAIN: songs_main()
#-----------------------------------------
@app.route("/main")
@login_required
def songs_main():
	return render_template("auth/welcome.html", db_index=find_database_status(), abv_average=Words.find_songs_authors_with_matches_geq_avg())


#-----------------------------------------
#		DB-STATUS: find_database_status()
#-----------------------------------------
def find_database_status():

	user_list = [g.user.id,1]

	stmt = text("SELECT DISTINCT Song.language, "
				"COUNT(DISTINCT Song.name), "
				"COUNT(DISTINCT Author.name) "
				"FROM Song "
				"LEFT JOIN author_song ON Song.id = author_song.song_id "
				"LEFT JOIN Author ON author_song.author_id = Author.id "
				"LEFT JOIN account ON account.id = Song.account_id "
				"WHERE account.id IN (:user1,:user2) "
				"GROUP BY Song.language "
				"ORDER BY Song.language ASC").params(user1=user_list[0],user2=user_list[1])

	result = db.engine.execute(stmt)

	response = []
	for row in result:
		response.append({'languages':row[0], 'songs':row[1], 'authors':row[2]})

	return response
	

#-----------------------------------------
#		SONGS: songs_list()
#-----------------------------------------
@app.route("/songs", methods=["GET", "POST"])
@login_required
def songs_list():
	song_list = [g.user.id,1]
	
	if request.method == "GET":
		songs = Song.query.filter(Song.account_id.in_((song_list))).all()

	if request.method == "POST":
		# sorting
		if request.form['sort'] == "titasc":
			songs = Song.query.filter(Song.account_id.in_((song_list))).order_by(Song.name.asc()).all()
		elif request.form['sort'] == "titdesc":
			songs = Song.query.filter(Song.account_id.in_((song_list))).order_by(Song.name.desc()).all()
		elif request.form['sort'] == "langtitasc":
			songs = Song.query.filter(Song.account_id.in_((song_list))).order_by(Song.language).order_by(Song.name.asc()).all()
		elif request.form['sort'] == "langtitdesc":
			songs = Song.query.filter(Song.account_id.in_((song_list))).order_by(Song.language).order_by(Song.name.desc()).all()
		else:
			songs = Song.query.filter(Song.account_id.in_((song_list))).all()

	return render_template("songs/list.html", songs=songs)


#-----------------------------------------
#		SONGS/SHOW: songs_show()
#-----------------------------------------
@app.route("/songs/show/<song_id>/", methods=["GET", "POST"])
@login_required
def songs_show(song_id):
	if request.method == "GET" and request.form.get("Back") == "Back":
		return render_template("songs/list.html", song = Song.query.filter_by(id=song.account_id).first())
	return render_template("songs/show.html", song = Song.query.get(song_id))


#-----------------------------------------
#		SONGS/EDIT: songs_edit()
#-----------------------------------------
@app.route("/songs/edit/<song_id>/", methods=["GET", "POST"])
@login_required
def songs_edit(song_id):
	form = SongForm(request.form)

	if request.form.get("Back") == "Back":
		return redirect(url_for("songs_list"))

	if request.method == "GET":
		return render_template("songs/edit.html", song = Song.query.get(song_id), form = form)
	elif request.method == "POST":
		if request.form.get("Submit") == "Submit":

			if not form.validate():
				return render_template("songs/edit.html", song = Song.query.get(song_id), form = form, error = "Fields must not be empty.")

			song = Song.query.get(song_id)
			song_name = request.form.get("name")
			song_lyrics = request.form.get("lyrics")
			song_language = request.form.get("language")
			song_author = request.form.get("author")
			if (song_name == song.name and song_author == song.author and song_lyrics == song.lyrics and song_language == song.language):
				flash("No changes made.", "warning")
			else:
				try:
					song = Song.query.filter_by(id=song_id).first()
					song.name = song_name
					song.lyrics = song_lyrics
					song.language = song_language
					song.author = song_author
					db.session().add(song)
					db.session().commit()
				except IntegrityError:
					db.session.rollback()
					flash("Song exists already.", "danger")
		return render_template("songs/edit.html", song = Song.query.get(song_id), form = form)
	return render_template("songs/list.html", song = Song.query.all())


#-----------------------------------------
#		SONGS/DELETE: songs_delete()
#-----------------------------------------
@app.route("/songs/delete/<song_id>", methods=["POST"])
@login_required
def songs_delete(song_id):
	qry = db.session().query(Song).filter(Song.id==song_id)
	if request.method == "POST":
		try:
			db.session().delete(qry.first())
			db.session().commit()
		except SQLAlchemyError:
			db.session.rollback()
			flash("Song not deleted.", "danger")
		return redirect('/songs')
	return render_template("songs/list.html", songs = Song.query.all())


#-----------------------------------------
#		SONGS/NEW: song_create()
#-----------------------------------------
@app.route("/songs/new/", methods=["GET", "POST"])
@login_required
def songs_create():
	form = SongForm(request.form)

	if request.method == "GET":
		return render_template("songs/new.html", form = form)

	language = SelectField('language', [DataRequired()],
		choices=[('', ''),
				('finnish', 'finnish'),
				('english', 'english'),
				('french', 'french')])

	if not form.validate():
		return render_template("songs/new.html", form = form, error = "Fields must not be empty.")

	song = Song(form.name.data,form.lyrics.data,form.language.data)
	song.account_id = g.user.id
	
	authors = form.author.data.split(',')
	for auth in authors:
		author = Author(auth)
	try:
		db.session().add(author)
		db.session().commit()
	except SQLAlchemyError:
		db.session.rollback()
		flash("Author(s) not added to database.", "danger")
		return render_template("songs/new.html", form = form)

	song.authors.extend([w for w in Author.query.filter_by(name=auth)])

	try:
		db.session().add(song)
		db.session().commit()
	except IntegrityError:
		db.session.rollback()
		flash("Song already exists. Consider changing name.", "warning")
		return render_template("songs/new.html", form = form)
	except SQLAlchemyError:
		db.session.rollback()
		flash("Something went wrong.", "danger")
		return render_template("songs/new.html", form = form)

	return render_template("songs/list.html", songs = Song.query.all())

