from flask import render_template#, session
from application import app

# def sumSessionCounter():
  # try:
    # session['counter'] += 1
  # except KeyError:
    # session['counter'] = 1

@app.route("/")
def index():
	# sumSessionCounter()
	return render_template("index.html")
