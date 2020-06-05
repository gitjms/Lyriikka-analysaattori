from flask import redirect, url_for, render_template, request, flash

from application import app, db, login_manager, login_required
from application.songs.models import Song
from application.auth.models import User
from application.authors.models import Author, author_song


#-----------------------------------------
#		AUTHORS: authors_list()
#-----------------------------------------
@app.route("/authors/list", methods=["GET", "POST"])
@login_required
def authors_list():

	if request.form.get("Back") == "Back":
		return redirect(url_for("songs_home"))

	authors = Author.find_authors()
	if authors:
		return render_template("authors/list.html", authors=authors)
	else:
		return render_template("authors/list.html", authors=None)


#-----------------------------------------
#		AUTHORS: authors_show()
#-----------------------------------------
@app.route("/authors/show/<author_id>/", methods=["GET", "POST"])
@login_required
def authors_show(author_id):

	if request.method == "GET":
		return render_template("authors/show.html", author = Author.query.get(author_id))

	if request.method == "POST":
		if request.form.get("Back") == "Back":
			return redirect(url_for("authors_list"))
