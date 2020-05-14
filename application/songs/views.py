from application import app, db
from flask import redirect, url_for, render_template, request, flash
from application.songs.models import Song
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/")
def songs_main():
	return render_template("index.html")


@app.route("/songs", methods=["GET", "POST"])
def songs_index():
	return render_template("songs/list.html", songs = Song.query.all())

@app.route("/songs/show/<song_id>/", methods=["GET", "POST"])
def songs_show(song_id):
	return render_template("songs/show.html", song = Song.query.get(str(song_id)))


@app.route("/songs", methods=["GET", "POST"])
def songs_delete(song_id):
	db.session().execute('DELETE FROM song WHERE id = ?'[int(song_id)])
	db.session().commit()
	flash('Song deleted')
	return render_template("songs/list.html", songs = Song.query.all())

@app.route("/songs/new/")
def songs_form():
	return render_template("songs/new.html")


@app.route("/songs/", methods=["POST"])
def song_create():
	n = Song(request.form.get("name"),request.form.get("text"))

	db.session().add(n)
	db.session().commit()

	return redirect(url_for("songs_index"))
