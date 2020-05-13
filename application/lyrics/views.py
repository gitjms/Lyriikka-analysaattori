from application import app, db
from flask import render_template, request
from application.lyrics.models import Song

@app.route("/lyrics/new/")
def lyrics_form():
	return render_template("lyrics/new.html")

@app.route("/lyrics/", methods=["POST"])
def lyrics_create():
	t = Song(request.form.get("name"))

	db.session().add(t)
	db.session().commit()

	return "hello world!"
