from application import app, db
from flask import redirect, url_for, render_template, request, flash
from flask_wtf import FlaskForm
from application.songs.models import Song
from application.songs.forms import SongForm
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

# Lomakkeen näyttämisen ja lähetyksen vastaanottava toiminnallisuus.

#-----------------------------------------
#		INDEX: songs_main()
#-----------------------------------------
@app.route("/")
def songs_main():
	return render_template("index.html")


#-----------------------------------------
#		LIST: songs_index()
#-----------------------------------------
@app.route("/songs", methods=["GET", "POST"])
def songs_index():
	#if request.method == "POST":
	#	if request.form.get("Back") == "Back":
	#		return redirect(url_for("songs_main"))
	return render_template("songs/list.html", songs = Song.query.all())


#-----------------------------------------
#		SHOW: songs_show()
#-----------------------------------------
@app.route("/songs/show/<song_id>/", methods=["GET", "POST"])
def songs_show(song_id):
	if request.method == "GET":
		if request.form.get("Back") == "Back":
			return render_template("songs/list.html", song = Song.query.all())
	return render_template("songs/show.html", song = Song.query.get(song_id))


#-----------------------------------------
#		EDIT: songs_edit()
#-----------------------------------------
@app.route("/songs/edit/<song_id>/", methods=["GET"])
def songs_edit():
	return render_template("songs/edit.html", form = SongForm())


#-----------------------------------------
#		EDIT: songs_edit()
#-----------------------------------------
@app.route("/songs/edit/<song_id>/", methods=["GET", "POST"])
def songs_editing(song_id):
	form = SongForm(request.form)

	if request.form.get("Back") == "Back":
		return redirect(url_for("songs_index"))

	if request.method == "GET":
		return render_template("songs/edit.html", song = Song.query.get(song_id), form = form)
	elif request.method == "POST":
		if request.form.get("Submit") == "Submit":

			if not form.validate():
				return render_template("songs/edit.html", song = Song.query.get(song_id), form = form)

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
					flash("Changes updated.", "success")
				except IntegrityError:
					db.session.rollback()
					flash("Song exists already.", "danger")
					pass
		return render_template("songs/edit.html", song = Song.query.get(song_id), form = form)
	return render_template("songs/list.html", song = Song.query.all())


#-----------------------------------------
#		DELETE: songs_delete()
#-----------------------------------------
@app.route("/songs/delete/<song_id>", methods=["POST"])
def songs_delete(song_id):
	qry = db.session().query(Song).filter(Song.id==song_id)
	if request.method == "POST":
		try:
			db.session().delete(qry.first())
			db.session().commit()
			flash("Song deleted.", "success")
		except SQLAlchemyError:
			db.session.rollback()
			flash("Song not deleted.", "danger")
			pass
		return redirect('/songs')
	return render_template("songs/list.html", songs = Song.query.all())


#-----------------------------------------
#		NEW: songs_new()
#-----------------------------------------
@app.route("/songs/new/", methods=["GET"])
def songs_new():
	return render_template("songs/new.html", form = SongForm())


#-----------------------------------------
#		CREATE: song_create()
#-----------------------------------------
@app.route("/songs/new/", methods=["POST"])
def song_create():
	form = SongForm(request.form)

	if request.form.get("Back") == "Back":
		return redirect(url_for("songs_index"))

	if not form.validate():
		return render_template("songs/new.html", form = form)

	song = Song(form.title.data,form.author.data,form.lyrics.data)
	try:
		db.session().add(song)
		db.session().commit()
		flash("Song added.", "success")
	except IntegrityError:
		db.session.rollback()
		flash("Song already exists. Consider changing title.", "danger")
		return render_template("songs/new.html", form = form)

	return render_template("songs/list.html", songs = Song.query.all())

