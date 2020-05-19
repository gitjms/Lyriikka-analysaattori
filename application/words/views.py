from flask import redirect, url_for, render_template, request, flash, g
from flask_wtf import FlaskForm
from flask_login import login_required, current_user

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from application import app, db
from application.songs.models import Song
from application.words.models import Words
from application.words.forms import WordForm

# Lomakkeen näyttämisen ja lähetyksen vastaanottava toiminnallisuus.

@app.before_request
def before_request():
	g.user = current_user


#-----------------------------------------
#		SHOW: words_find()
#-----------------------------------------
@app.route("/words/show/", methods=["GET", "POST"])
@login_required
def words_find():
	form = WordForm(request.form)

	if request.method == "GET":
		return render_template(request.args.get('next') or "songs/words.html", form = form)

	if request.form.get("Back") == "Back":
		return redirect(url_for("songs_index"))

	if not form.validate():
		return render_template(request.args.get('next') or "songs/words.html", form = form)

	words = form.title.data

	return render_template("songs/words.html", song = Song.query.filter_by(words=words))
