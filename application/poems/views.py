from flask import redirect, url_for, render_template, request, flash, g
from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired
from flask_login import current_user

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.sql import text
from sqlalchemy import func, distinct, asc

from application import app, db, login_manager, login_required
from application.poems.models import Poem
from application.auth.models import User
from application.words.models import Words
from application.poets.views import poets_list
from application.poets.models import Poet, poet_poem
from application.poems.forms import NewPoemForm, EditPoemForm


@app.before_request
def before_request():
	g.user = current_user


#-----------------------------------------
#		SONGS: poems_list()
#-----------------------------------------
@app.route("/poems/list", methods=["GET", "POST"])
@login_required(roles=[1,2,3])
def poems_list():
	
	if request.method == "GET":
		poems = Poem.query.filter(Poem.account_id==g.user.id or Poem.account_role==1).all()

		if not poems:
			return render_template("poems/list.html", poems=None, top_words=None)

	if request.method == "POST":
		# sorting
		if request.form.get("sort") == "titasc":
			poems = Poem.query.filter(Poem.account_id==g.user.id or Poem.account_role==1).order_by(Poem.name.asc()).all()
		elif request.form.get("sort") == "titdesc":
			poems = Poem.query.filter(Poem.account_id==g.user.id or Poem.account_role==1).order_by(Poem.name.desc()).all()
		elif request.form.get("sort") == "langtitasc":
			poems = Poem.query.filter(Poem.account_id==g.user.id or Poem.account_role==1).order_by(Poem.language).order_by(Poem.name.asc()).all()
		elif request.form.get("sort") == "langtitdesc":
			poems = Poem.query.filter(Poem.account_id==g.user.id or Poem.account_role==1).order_by(Poem.language).order_by(Poem.name.desc()).all()
		elif request.form.get("sort") == "id":
			poems = Poem.query.filter(Poem.account_id==g.user.id or Poem.account_role==1).order_by(Poem.id.asc()).all()

	return render_template("poems/list.html", poems=poems)


#-----------------------------------------
#		SONGS/SHOW: poems_show()
#-----------------------------------------
@app.route("/poems/show/<poem_id>/<poet_id>/<from_page>", methods=["GET", "POST"])
@login_required(roles=[1,2,3])
def poems_show(poem_id,poet_id,from_page):

	if request.method == "POST":
		if request.form.get("Back") == "Back":
			if from_page == 'poems':
				return redirect(url_for("poems_list"))
			elif from_page == 'poets':
				return redirect(url_for("poets_show", poet_id = poet_id))
			elif from_page == 'edit':
				return redirect(url_for("poems_list"))

	if request.method == "GET":
		return render_template("poems/show.html", poem = Poem.query.get(poem_id), poem_id=poem_id, poet_id=poet_id, from_page=from_page)


#-----------------------------------------
#		SONGS/EDIT: poems_edit()
#-----------------------------------------
@app.route("/poems/edit/<poem_id>/<poet_id>/<from_page>", methods=["GET", "POST"])
@login_required(roles=[1,3])
def poems_edit(poem_id,poet_id,from_page):

	form = EditPoemForm(request.form)
	
	poem = Poem.query.get(poem_id)
	form.language.default = poem.language
	form.process()

	if request.form.get("Back") == "Back":
		if from_page == 'poems':
			return redirect(url_for("poems_list"))
		elif from_page == 'poets':
			return redirect(url_for('poems_show', poem_id=poem_id, poet_id=poet_id, from_page=from_page))

	if request.form.get("Edit") == "Edit":
		return render_template("poems/edit.html", poem=poem, form=form, poem_id=poem_id, poet_id=poet_id, from_page=from_page)

	elif request.method == "POST":

		if request.form.get("Submit") == "Submit":
			form = EditPoemForm(request.form)
			
			if not form.validate():
				return render_template("poems/edit.html", poem=poem, form=form, poem_id=poem_id, poet_id=poet_id, from_page=from_page, error="Fields must not be empty.")

			new_name = form.title.data.strip()
			new_lyrics = form.lyrics.data.strip()
			new_poet = form.poet.data.strip()
			new_language = form.language.data

			old_name = poem.name.strip()
			old_lyrics = poem.lyrics.strip()
			old_poet = poem.poets
			old_language = poem.language

			if (new_name == old_name and new_lyrics == old_lyrics and new_poet == old_poet and new_language == old_language):
				flash("No changes made.", "warning")
				return render_template("poems/edit.html", poem=poem, form=form, poem_id=poem_id, poet_id=poet_id, from_page=from_page)

			if new_poet != old_poet:
				if Poet.query.filter_by(name=new_poet.strip()) is None:
					poet = Poet(name=new_poet.strip())
					try:
						db.session().add(poet)
						db.session().commit()
					except SQLAlchemyError:
						db.session.rollback()
						flash("Poet not added to database.", "danger")
			try:
				if new_name != old_name:
					poem.name = new_name
				if new_lyrics != old_lyrics:
					poem.lyrics = new_lyrics
				if new_poet.strip() != old_poet:
					poem.poets.extend(Poet.query.filter_by(name=new_poet.strip()))
				if new_language != old_language:
					poem.language = new_language

				db.session().commit()
				return redirect(url_for("poems_show", poem_id=poem_id, poet_id=poet_id, from_page=from_page))
			except SQLAlchemyError:
				db.session.rollback()
				flash("Poem exists already.", "danger")

			return render_template("poems/edit.html", poem=poem, form=form, poem_id=poem_id, poet_id=poet_id, from_page=from_page)

	return redirect(url_for("poems_list"))


#-----------------------------------------
#		SONGS/DELETE: poems_delete()
#-----------------------------------------
@app.route("/poems/delete/<poem_id>", methods=["GET","POST"])
@login_required(roles=[1,3])
def poems_delete(poem_id):

	if request.method == "GET":
		return

	qry = db.session().query(Poem).filter(Poem.id==poem_id)
	if request.method == "POST":
		try:
			db.session().delete(qry.first())
			db.session().commit()
		except SQLAlchemyError:
			db.session.rollback()
			flash("Poem not deleted.", "danger")

	return redirect(url_for("poems_list"))


#-----------------------------------------
#		POEMS/NEW: poem_create()
#-----------------------------------------
@app.route("/poems/new/", methods=["GET", "POST"])
@login_required(roles=[1,3])
def poems_create():

	form = NewPoemForm(request.form)

	if request.method == "GET":
		return render_template("poems/new.html", form=form)

	language = SelectField('language', [DataRequired()],
		choices=[('', ''),
				('finnish', 'finnish'),
				('english', 'english'),
				('french', 'french')])

	if not form.validate():
		return render_template("poems/new.html", form=form, error="Fields must not be empty.")

	poem = Poem(form.title.data,form.lyrics.data,form.language.data)
	poem.account_id = g.user.id
	poem.account_role = g.user.role
	
	new_poet_name = request.form["poet"]
	old_poet = Poet.query.filter_by(name=new_poet_name.strip()).first()
	if old_poet is None:
		new_poet = Poet(name=new_poet_name.strip(),result_all=None,result_no_stop_words=None)
		try:
			db.session().add(new_poet)
			db.session().commit()
		except SQLAlchemyError:
			db.session.rollback()
			flash("Poet not added to database.", "danger")
			return render_template("poems/new.html", form=form)

		poem.poets.extend(db.session.query(Poet).filter(Poet.name==new_poet_name))

	try:
		db.session().add(poem)
		db.session().commit()
	except IntegrityError:
		db.session.rollback()
		flash("Poem already exists. Consider changing name.", "warning")
		return render_template("poems/new.html", form=form)
	except SQLAlchemyError:
		db.session.rollback()
		flash("Something went wrong.", "danger")
		return render_template("poems/new.html", form=form)

	return render_template("poems/list.html", poems=Poem.query.all())

