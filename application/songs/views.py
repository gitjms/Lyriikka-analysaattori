from flask import redirect, url_for, render_template, request, flash, g
from flask_wtf import FlaskForm
from flask_login import login_required, current_user

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from application import app, db
from application.songs.models import Song
from application.authors.models import Author
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
#		LIST: songs_list()
#-----------------------------------------
@app.route("/songs", methods=["GET", "POST"])
@login_required
def songs_list():
	song_list = [g.user.id,1]
	return render_template("songs/list.html", songs = Song.query.filter(Song.account_id.in_((song_list))))


#-----------------------------------------
#		SHOW: songs_show()
#-----------------------------------------
@app.route("/songs/show/<song_id>/", methods=["GET", "POST"])
@login_required
def songs_show(song_id):
	if request.method == "GET" and request.form.get("Back") == "Back":
		return render_template("songs/list.html", song = Song.query.filter_by(id=song.account_id).first())
	return render_template("songs/show.html", song = Song.query.get(song_id))


#-----------------------------------------
#		EDIT: songs_edit()
#-----------------------------------------
@app.route("/songs/edit/<song_id>/", methods=["GET", "POST"])
@login_required
def songs_editing(song_id):
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
			song_title = request.form.get("title")
			song_author = request.form.get("author")
			song_lyrics = request.form.get("lyrics")
			if (song_title == song.title and song_author == song.author and song_lyrics == song.lyrics):
				flash("No changes made.", "warning")
			else:
				try:
					song = Song.query.filter_by(id=song_id).first()
					song.title = song_title
					song.author = song_author
					song.lyrics = song_lyrics
					db.session().add(song)
					db.session().commit()
				except IntegrityError:
					db.session.rollback()
					flash("Song exists already.", "danger")
		return render_template("songs/edit.html", song = Song.query.get(song_id), form = form)
	return render_template("songs/list.html", song = Song.query.all())


#-----------------------------------------
#		DELETE: songs_delete()
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
#		CREATE: song_create()
#-----------------------------------------
@app.route("/songs/new/", methods=["GET", "POST"])
@login_required
def songs_create():
	form = SongForm(request.form)

	if request.method == "GET":
		return render_template("songs/new.html", form = form)

	if not form.validate():
		return render_template("songs/new.html", form = form, error = "Fields must not be empty.")

	song = Song(form.title.data,form.lyrics.data)
	song.account_id = g.user.id
	
	authors = form.author.data.split(',')
	new_authors = [w for w in Author(authors)]
	song.author.extend(new_authors)
	
	try:
		db.session().add(song)
		db.session().commit()
	except IntegrityError:
		db.session.rollback()
		flash("Song already exists. Consider changing title.", "danger")
		return render_template("songs/new.html", form = form)

	return render_template("songs/list.html", songs = Song.query.all())
