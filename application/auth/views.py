from flask import render_template, request, redirect, url_for, flash, g, session
from flask_login import login_user, logout_user, current_user

import bcrypt as hash_bcrypt
from flask_bcrypt import Bcrypt

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.sql import text

from application import app, db, login_required
from application.auth.models import User
from application.songs.models import Song
from application.words.models import Words
from application.auth.forms import LoginForm
from application.auth.forms import CreateUserForm


bcrypt = Bcrypt()

@app.before_request
def before_request():
	g.user = current_user


#-----------------------------------------
#		STATS: auth_stats()
#-----------------------------------------
@app.route("/auth/stats", methods = ["GET"])
@login_required
def auth_stats():

	errors = []

	# TOP 5 search words
	words = Words.find_words()
	stats = Words.find_stats()
	result_list = []

	for i in range(len(words)):
		new_list = []
		new_list.append(words[i]['word'])
		new_list.append(words[i]['count'])
		new_list.append(stats[i]['matches'])
		new_list.append(stats[i]['average'])
		result_list.append(new_list)

	db_status=Song.find_database_status()
	if db_status:
		return render_template("auth/stats.html", db_status=db_status, top_words=result_list)
	else:
		errors.append("Cannot load database status.")
		return render_template("auth/stats.html", db_status=None, top_words=result_list, errors=errors)


#-----------------------------------------
#		LOGIN: auth_login()
#-----------------------------------------
@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
	form = LoginForm(request.form)
	
	if g.user.is_authenticated:
		return redirect(url_for("index"))

	if request.method == "GET":
		return render_template("auth/loginform.html", form = form)

	remember_me = False
	if 'remember_me' in request.form:
		remember_me = True

	if request.form.get("Guest") == "Guest":
		username = "guest"
		password = u"guest".encode('utf-8')
	elif request.form.get("Login") == "Login":
		if not form.validate():
			return render_template("auth/loginform.html", form = form, error = "Fields must not be empty. Check password length.")

		username = form.username.data
		password = form.password.data.encode('utf-8')

	user = User.query.filter_by(username=username).first()
	if not user:
		flash("No such username or password.", "warning")
		return render_template("auth/loginform.html", form = form)

	true_password = hash_bcrypt.hashpw(user.password.encode('utf-8'), hash_bcrypt.gensalt())

	# Compare Password with hashed password
	if not hash_bcrypt.checkpw(password,true_password):
		flash("No such password.", "warning")
		return render_template("auth/loginform.html", form = form)

	try:
		login_user(user, remember = remember_me)
	except IntegrityError:
		flash("Problems with login.", "danger")
		return render_template("auth/loginform.html", form = form)
		
	db.session.permanent = remember_me

	return redirect(url_for("index"))


#-----------------------------------------
#		CREATE: user_create()
#-----------------------------------------
@app.route("/auth/newuser/", methods=["GET", "POST"])
def auth_create():
	form = CreateUserForm(request.form)

	if request.method == "GET":
		return render_template("auth/newuser.html", form = form)

	if not form.validate_on_submit():
		return render_template("auth/newuser.html", form = form)

	pw_hash = bcrypt.generate_password_hash(form.password.data)
	
	user = User(form.name.data,form.username.data,form.password.data)
	user.role = "USER"

	try:
		db.session().add(user)
		db.session().commit()
		login_user(user)
	except IntegrityError:
		db.session.rollback()
		flash("Create account failed.", "danger")
		return render_template("auth/newuser.html", form = form, error = "User already exists. Consider changing username.")

	return redirect(url_for("index"))


#-----------------------------------------
#		LOGOUT: auth_logout()
#-----------------------------------------
@app.route("/auth/logout")
def auth_logout():
	logout_user()
	return redirect(url_for("index"))
