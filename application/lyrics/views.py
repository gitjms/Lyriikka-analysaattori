from application import app, db
from flask import render_template, request
from application.lyrics.models import Song

@app.route("/lyrics", methods=["GET"])
def tasks_index():
	return render_template("lyrics/list.html", lyrics = Song.query.all())

@app.route("/lyrics/new/")
def lyrics_form():
	return render_template("lyrics/new.html")

@app.route("/lyrics/", methods=["POST"])
def lyrics_create():
	n = Song(request.form.get("name"))
	#t = Song(request.form.get("text"))

	db.session().add(n)
	db.session().commit()

	return redirect(url_for("lyrics_index"))
