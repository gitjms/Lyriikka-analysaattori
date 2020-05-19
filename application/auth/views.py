from flask import render_template, request, redirect, url_for, flash, g, session
from flask_login import login_user, logout_user, current_user, login_required

import bcrypt as hash_bcrypt
from flask_bcrypt import Bcrypt

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from application import app, db
from application.auth.models import User
from application.auth.forms import LoginForm, CreateForm

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

	if request.form.get("Back") == "Back":
		return redirect(url_for("index"))

	if request.method == "GET":
		return render_template("auth/loginform.html", form = form)

	remember_me = False
	if 'remember_me' in request.form:
		flash("remembered.", "success")
		remember_me = True

	if request.form.get("Guest") == "Guest":
		username = "guest"
		password = u"guest".encode('utf-8')
	elif request.form.get("Login") == "Login":
		if not form.validate():
			flash("Login failed.", "warning")
			return render_template("auth/loginform.html", form = form)

		username = form.username.data
		password = form.password.data.encode('utf-8')

	user = User.query.filter_by(username=username).first()
	if not user:
		flash("No such username or password.", "warning")
		return render_template("auth/loginform.html", form = form)

	true_password = hash_bcrypt.hashpw(user.password.encode('utf-8'), hash_bcrypt.gensalt())

	# Compare Password with hashed password
	if hash_bcrypt.checkpw(password,true_password) == False:
		flash("No such username or password.", "warning")
		return render_template("auth/loginform.html", form = form)

	flash("User " + user.username + " identified.", "success")
	login_user(user, remember = remember_me)
	db.session.permanent = True
	session['user_id'] = user.id

	return redirect(request.args.get('next') or url_for("index"))


#-----------------------------------------
#		CREATE: user_create()
#-----------------------------------------
@app.route("/auth/newuser/", methods=["GET", "POST"])
def auth_create():
	form = CreateForm(request.form)

	if request.method == "GET":
		return render_template("auth/newuser.html", form = form)

	if request.form.get("Back") == "Back":
		return redirect(url_for("index"))

	if not form.validate():
		return render_template("auth/newuser.html", form = form, error = "Check your password.")

	pw_hash = bcrypt.generate_password_hash(form.password.data)
	
	user = User(form.fullname.data,form.username.data,form.password.data,False)

	remember_me = False
	if 'remember_me' in request.form:
		flash_text = "User added and logged in. Session remembered."
		remember_me = True
	else:
		flash_text = "User added and logged in."

	try:
		db.session().add(user)
		db.session().commit()
		login_user(user, remember = remember_me)
		db.session.permanent = True
		flash(flash_text, "success")
	except IntegrityError:
		db.session.rollback()
		flash("User already exists. Consider changing username.", "danger")
		return render_template("auth/newuser.html", form = form)

	return redirect(request.args.get('next') or url_for("index"))


#-----------------------------------------
#		LOGOUT: auth_logout()
#-----------------------------------------
@app.route("/auth/logout")
def auth_logout():
	logout_user()
	return redirect(url_for("index"))
