from flask import redirect, url_for, render_template, request, flash, g
from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired
from flask_login import current_user

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.sql import text
from sqlalchemy import func, distinct, asc, or_

from application import app, db, login_manager, login_required
from application.songs.models import Song
from application.auth.models import User
from application.authors.views import authors_list
from application.authors.models import Author, author_song
from application.songs.forms import NewSongForm, EditSongForm


@app.before_request
def before_request():
	g.user = current_user


#-----------------------------------------
#		SONGS: songs_list()
#-----------------------------------------
@app.route("/songs/list", methods=["GET", "POST"])
@login_required(roles=[1,2,3])
def songs_list():
	
	if request.method == "GET":
		songs = Song.query.filter(or_(Song.account_id==g.user.id,Song.account_role==1)).all()
		
		if not songs:
			return render_template("songs/list.html", songs=None, top_words=None)

	if request.method == "POST":
		# sorting
		if request.form.get("sort") == "titasc":
			songs = Song.query.filter(or_(Song.account_id==g.user.id,Song.account_role==1)).order_by(Song.name.asc()).all()
		elif request.form.get("sort") == "titdesc":
			songs = Song.query.filter(or_(Song.account_id==g.user.id,Song.account_role==1)).order_by(Song.name.desc()).all()
		elif request.form.get("sort") == "langtitasc":
			songs = Song.query.filter(or_(Song.account_id==g.user.id,Song.account_role==1)).order_by(Song.language).order_by(Song.name.asc()).all()
		elif request.form.get("sort") == "langtitdesc":
			songs = Song.query.filter(or_(Song.account_id==g.user.id,Song.account_role==1)).order_by(Song.language).order_by(Song.name.desc()).all()
		elif request.form.get("sort") == "id":
			songs = Song.query.filter(or_(Song.account_id==g.user.id,Song.account_role==1)).order_by(Song.id.asc()).all()

	return render_template("songs/list.html", songs=songs)


#-----------------------------------------
#		SONGS/SHOW: songs_show()
#-----------------------------------------
@app.route("/songs/show/<song_id>/<author_id>/<from_page>", methods=["GET", "POST"])
@login_required(roles=[1,2,3])
def songs_show(song_id,author_id,from_page):

	if request.method == "POST":
		if request.form.get("Back") == "Back":
			if from_page == 'songs':
				return redirect(url_for("songs_list"))
			elif from_page == 'authors':
				return redirect(url_for("authors_show", author_id = author_id))
			elif from_page == 'edit':
				return redirect(url_for("songs_list"))

	if request.method == "GET":
		return render_template("songs/show.html", song = Song.query.get(song_id), song_id=song_id, author_id=author_id, from_page=from_page)


#-----------------------------------------
#		SONGS/EDIT: songs_edit()
#-----------------------------------------
@app.route("/songs/edit/<song_id>/<author_id>/<from_page>", methods=["GET", "POST"])
@login_required(roles=[1,3])
def songs_edit(song_id,author_id,from_page):

	form = EditSongForm(request.form)
	
	song = Song.query.get(song_id)
	form.language.default = song.language
	form.process()

	if request.form.get("Back") == "Back":
		if from_page == 'songs':
			return redirect(url_for("songs_list"))
		elif from_page == 'authors':
			return redirect(url_for('songs_show', song_id=song_id, author_id=author_id, from_page=from_page))

	if request.form.get("Edit") == "Edit":
		return render_template("songs/edit.html", song=song, form=form, song_id=song_id, author_id=author_id, from_page=from_page)

	elif request.method == "POST":

		if request.form.get("Submit") == "Submit":
			form = EditSongForm(request.form)
			
			if not form.validate():
				return render_template("songs/edit.html", song=song, form=form, song_id=song_id, author_id=author_id, from_page=from_page, error="Fields must not be empty.")

			new_name = form.title.data
			new_lyrics = form.lyrics.data
			new_authors = [w.strip() for w in form.author.data.split(',')]
			new_language = form.language.data

			old_name = song.name
			old_lyrics = song.lyrics
			old_authors = [w.name for w in song.authors]
			old_language = song.language

			if (new_name == old_name and new_lyrics == old_lyrics and new_authors == old_authors and new_language == old_language):
				flash("No changes made.", "warning")
				return render_template("songs/edit.html", song=song, form=form, song_id=song_id, author_id=author_id, from_page=from_page)

			if new_authors != old_authors:
				for auth in new_authors:
					if Author.query.filter_by(name=auth.strip()).first() is None:
						author = Author(name=auth.strip(),result_all=None,result_no_stop_words=None)
						try:
							db.session().add(author)
							db.session().commit()
						except SQLAlchemyError:
							db.session.rollback()
							flash("Author(s) not added to database.", "danger")
			try:
				if new_name != old_name:
					song.name = new_name
				if new_lyrics != old_lyrics:
					song.lyrics = new_lyrics
				for auth in new_authors:
					if auth.strip() not in old_authors:
						song.authors.extend(Author.query.filter_by(name=auth.strip()))
				if new_language != old_language:
					song.language = new_language

				db.session().commit()
				return redirect(url_for("songs_show", song_id=song_id, author_id=author_id, from_page=from_page))
			except SQLAlchemyError:
				db.session.rollback()
				flash("Song exists already.", "danger")

			return render_template("songs/edit.html", song=song, form=form, song_id=song_id, author_id=author_id, from_page=from_page)

	return redirect(url_for("songs_list"))


#-----------------------------------------
#		SONGS/DELETE: songs_delete()
#-----------------------------------------
@app.route("/songs/delete/<song_id>", methods=["GET","POST"])
@login_required(roles=[1,3])
def songs_delete(song_id):

	if request.method == "GET":
		return

	song_query = db.session().query(Song).filter(Song.id==song_id)
	if request.method == "POST":
		try:
			db.session().delete(song_query.first())
			db.session().commit()
		except SQLAlchemyError:
			db.session.rollback()
			flash("Song not deleted.", "danger")

	return redirect(url_for("songs_list"))


#-----------------------------------------
#		SONGS/NEW: song_create()
#-----------------------------------------
@app.route("/songs/new/", methods=["GET", "POST"])
@login_required(roles=[1,3])
def songs_create():

	form = NewSongForm(request.form)

	if request.method == "GET":
		return render_template("songs/new.html", form = form)

	language = SelectField('language', [DataRequired()],
		choices=[('', ''),
				('finnish', 'finnish'),
				('english', 'english'),
				('french', 'french')])

	if not form.validate():
		return render_template("songs/new.html", form = form, error = "Fields must not be empty.")

	song = Song(form.title.data,form.lyrics.data,form.language.data,g.user.id,g.user.role_id)
	
	authors = request.form["author"].split(',')
	for auth in authors:
		if Author.query.filter_by(name=auth.strip()).first() is None:
			author = Author(name=auth.strip(),result_all=None,result_no_stop_words=None)
			try:
				db.session().add(author)
				db.session().commit()
			except SQLAlchemyError:
				db.session.rollback()
				flash("Author(s) not added to database.", "danger")
				return render_template("songs/new.html", form = form)

	for auth in authors:
		song.authors.extend(Author.query.filter_by(name=auth.strip()))

	try:
		db.session().add(song)
		db.session().commit()
	except IntegrityError:
		db.session.rollback()
		flash("Song already exists. Consider changing name.", "warning")
		return render_template("songs/new.html", form = form)
	except SQLAlchemyError:
		db.session.rollback()
		flash("Something went wrong.", "danger")
		return render_template("songs/new.html", form = form)

	return render_template("songs/list.html", songs = Song.query.all())

