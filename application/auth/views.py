from flask import render_template, request, redirect, url_for, flash, g, session
from flask_login import login_user, logout_user, current_user, login_required

import bcrypt as hash_bcrypt
from flask_bcrypt import Bcrypt

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from application import app, db
from application.auth.models import User
from application.songs.models import Song
from application.words.models import Words
from application.auth.forms import LoginForm
from application.auth.forms import CreateForm

# Lomakkeen näyttämisen ja lähetyksen vastaanottava toiminnallisuus.

bcrypt = Bcrypt()

@app.before_request
def before_request():
	g.user = current_user


#-----------------------------------------
#		LOGIN: auth_login()
#-----------------------------------------
@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
	form = LoginForm(request.form)

	if request.method == "GET":
		return render_template("auth/loginform.html", form = form)

	if request.form.get("Back") == "Back":
		return redirect(url_for("index"))

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
	if hash_bcrypt.checkpw(password,true_password) == False:
		flash("No such password.", "warning")
		return render_template("auth/loginform.html", form = form)

	try:
		login_user(user, remember = remember_me)
	except IntegrityError:
		flash("Problems with login.", "danger")
		return render_template("auth/loginform.html", form = form)
		
	db.session.permanent = remember_me

	return redirect(url_for("songs_main"))


#-----------------------------------------
#		CREATE: user_create()
#-----------------------------------------
@app.route("/auth/newuser/", methods=["GET", "POST"])
def auth_create():
	form = CreateForm(request.form)

	if request.method == "GET":
		return render_template("auth/newuser.html", form = form)

	if request.form.get("Back") == "Back":
		return redirect(url_for("index.html"))

	remember_me = False
	if 'remember_me' in request.form:
		remember_me = True

	if not form.validate_on_submit():
		flash("Create account failed.", "warning")
		return render_template("auth/newuser.html", form = form, error = "Fields must not be empty. Check password length.")

	pw_hash = bcrypt.generate_password_hash(form.password.data)
	
	user = User(form.name.data,form.username.data,form.password.data,False)

	try:
		db.session().add(user)
		db.session().commit()
		login_user(user, remember = remember_me)
		db.session.permanent = remember_me
	except IntegrityError:
		db.session.rollback()
		flash("Failed.", "danger")
		return render_template("auth/newuser.html", form = form, error = "User already exists. Consider changing username.")

	return redirect(url_for("index"))


#-----------------------------------------
#		LOGOUT: auth_logout()
#-----------------------------------------
@app.route("/auth/logout")
def auth_logout():
	logout_user()
	return redirect(url_for("index"))
