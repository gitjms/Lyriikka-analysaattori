from application import app, db
from flask import redirect, url_for, render_template, request, flash
from application.songs.models import Song


@app.route("/")
def songs_main():
	return render_template("index.html")


@app.route("/songs", methods=["GET", "POST"])
def songs_index():
	return render_template("songs/list.html", songs = Song.query.all())

@app.route("/songs/show/<song_id>/", methods=["GET", "POST"])
def songs_show(song_id):
	return render_template("songs/show.html", song = Song.query.get(song_id))


@app.route("/songs/edit/<song_id>/", methods=["GET", "POST"])
def songs_edit(song_id):
	if request.method == "GET":
		if request.form.get("Back") == "Back":
			return redirect(url_for("songs_index"))
		return render_template("songs/edit.html", song = Song.query.get(song_id))
	elif request.method == "POST":
		if request.form.get("Back") == "Back":
			return redirect(url_for("songs_index"))
		song_name = request.form.get("name")
		song_author = request.form.get("author")
		song_text = request.form.get("text")
		if request.form.get("Submit") == "Submit":
			n = Song(song_name, song_author, song_text)
			song = Song.query.get(song_id)
			song.name = song_name
			song.author = song_author
			song.text = song_text
			db.session().commit()
			flash("Data updated.")
		return render_template("songs/edit.html", song = Song.query.get(song_id))
	return render_template("songs/list.html", song = Song.query.all())


# @app.route("/edit", methods=["GET", "POST"])
# def songs_editsong(song_id,name, author, text):
	# if request.method == "POST":
		# if request.form.get("Submit") == "Submit":
			# n = Song(name, author, text)
			# db.session().add(n)
			# db.session().commit()
			# flash("Data updated.")


@app.route("/delete/<song_id>", methods=["POST"])
def songs_delete(song_id):
	qry = db.session().query(Song).filter(Song.id==song_id)
	if request.method == "POST":
		db.session().delete(qry.first())
		db.session().commit()
		return redirect('/songs')
	return render_template("songs/list.html", songs = Song.query.all())

@app.route("/songs/new/", methods=["GET"])
def songs_form():
	return render_template("songs/new.html")


@app.route("/songs/", methods=["POST"])
def song_create():
	n = Song(request.form.get("name"),
		request.form.get("author"),
		request.form.get("text"))

	db.session().add(n)
	db.session().commit()

	return redirect(url_for("songs_index"))
