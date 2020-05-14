from application import app, db
from flask import redirect, url_for, render_template, request
from application.songs.models import Song


@app.route("/songs", methods=["GET"])
def songs_index():
	return render_template("songs/list.html", songs = Song.query.all())


@app.route("/songs/show/<songs_id>/", methods=["GET"])
def songs_show(songs_id):
	return render_template("songs/show.html", songs = Song.query.get(str(songs_id)))


@app.route("/songs/new/")
def songs_form():
	return render_template("songs/new.html")


@app.route("/songs/", methods=["POST"])
def songs_create():
	n = Song(request.form.get("name"),request.form.get("text"))

	db.session().add(n)
	db.session().commit()

	return redirect(url_for("songs_index"))
