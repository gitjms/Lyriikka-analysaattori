from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user

from application import app
from application.auth.models import User
from application.auth.forms import LoginForm

# Lomakkeen näyttämisen ja lähetyksen vastaanottava toiminnallisuus.

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

	if not form.validate():
		flash("You may login with guest account. Username: user, Password: user", "warning")
		return render_template("auth/loginform.html", form = form)

	user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
	if not user:
		flash("No such username or password.", "warning")
		return render_template("auth/loginform.html", form = form, error = "No such username or password")


	flash("User " + user.name + " identified.", "success")
	login_user(user)
	return redirect(url_for("index"))


#-----------------------------------------
#		LOGOUT: auth_logout()
#-----------------------------------------
@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))
