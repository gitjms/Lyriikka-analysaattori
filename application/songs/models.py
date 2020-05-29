from application import db
from application import views
from application import app
from flask import g
from flask_login import current_user
from sqlalchemy.sql import text
from application.models import Base


class Song(Base):

	__tablename__ = 'song'

	# id = db.Column(db.Integer, primary_key=True)
	# name = db.Column(db.String(80), nullable=False, unique=True)
	lyrics = db.Column(db.String(2000), nullable=False)
	language = db.Column(db.String(80), nullable=False)

	account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)


	def __init__(self, name, lyrics, language):
		self.name = name
		self.lyrics = lyrics
		self.language = language

