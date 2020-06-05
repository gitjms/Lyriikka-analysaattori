from flask import url_for, render_template, request, g
from flask_login import login_required, current_user

from application import app


@app.before_request
def before_request():
	g.user = current_user

@app.route("/")
def index():
	
	return render_template("index.html")


@app.route("/info")
def songs_info():

	return render_template("info.html")

