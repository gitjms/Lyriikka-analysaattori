from application import app, db
from flask import redirect, url_for, render_template, request, flash
from application.songs.models import Song
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

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
	return render_template("songs/list.html", songs = Song.query.all())


#-----------------------------------------
#		SHOW: songs_show()
#-----------------------------------------
@app.route("/songs/show/<song_id>/", methods=["GET", "POST"])
def songs_show(song_id):
	return render_template("songs/show.html", song = Song.query.get(song_id))


#-----------------------------------------
#		EDIT: songs_edit()
#-----------------------------------------
@app.route("/songs/edit/<song_id>/", methods=["GET", "POST"])
def songs_edit(song_id):
	if request.method == "GET":
		if request.form.get("Back") == "Back":
			return redirect(url_for("songs_index"))
		return render_template("songs/edit.html", song = Song.query.get(song_id))
	elif request.method == "POST":
		if request.form.get("Back") == "Back":
			return redirect(url_for("songs_index"))
		if request.form.get("Submit") == "Submit":
			song_name = request.form.get("name").strip()
			song_author = request.form.get("author").strip()
			song_text = request.form.get("text").strip()
			if (song_name and song_author and song_text):
				song = Song.query.get(song_id)
				song.name = song_name
				song.author = song_author
				song.text = song_text
				try:
					db.session().add(song)
					db.session().commit()
					flash("Data updated.", "success")
				except exc.SQLAlchemyError:
					db.session.rollback()
					flash("Data not updated", "danger")
					pass
			else:
				flash("No empty strings.", "warning")
		return render_template("songs/edit.html", song = Song.query.get(song_id))
	return render_template("songs/list.html", song = Song.query.all())


#-----------------------------------------
#		DELETE: songs_delete()
#-----------------------------------------
@app.route("/delete/<song_id>", methods=["POST"])
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
	return render_template("songs/new.html")


#-----------------------------------------
#		CREATE: song_create()
#-----------------------------------------
@app.route("/songs/", methods=["POST"])
def song_create():
	if request.form.get("Back") == "Back":
		return redirect(url_for("songs_index"))
	song_name = request.form.get("name").strip()
	song_author = request.form.get("author").strip()
	song_text = request.form.get("text").strip()
	if (song_name and song_author and song_text):
		song = Song(song_name,song_author,song_text)
		try:
			db.session().add(song)
			db.session().commit()
			flash("Song added.", "success")
		except SQLAlchemyError:
			db.session.rollback()
			flash("Song exists already.", "danger")
			pass
		except IntegrityError:
			db.session.rollback()
			flash("Song exists already.", "danger")
			pass
			
	else:
		flash("No empty strings.", "warning")

	return render_template("songs/list.html", songs = Song.query.all())

