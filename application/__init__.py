from flask import Flask
app = Flask(__name__)


from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lyrics.db"
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

from application import views

from application.lyrics import models
from application.lyrics import views

db.create_all()
