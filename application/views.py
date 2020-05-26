from flask import url_for, render_template, request, g
from flask_login import login_required, current_user

from application import app


@app.before_request
def before_request():
	g.user = current_user

@app.route("/", methods=["GET"])
def index():
	
	if request.method == "GET":
		return render_template("index.html")

