from flask import Flask
app = Flask(__name__)

import os
from flask_sqlalchemy import SQLAlchemy

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
	app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///songs.db"
	app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

from application import views

from application.songs import models
from application.songs import views
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

db.create_all()
