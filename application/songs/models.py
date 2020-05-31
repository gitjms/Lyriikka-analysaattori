from application import db
from application import views
from application import app
from flask import g
from flask_login import current_user
from sqlalchemy.sql import text
from application.models import Base


# join table SONG_RESULTS
song_result = db.Table('song_result', Base.metadata,
	db.Column(	'song_id',								# left
				db.ForeignKey('song.id', ondelete='cascade'),
				primary_key=True),
	db.Column(	'results_id',							# right
				db.ForeignKey('results.id', ondelete='cascade'),
				primary_key=True)
)


class Song(Base):

	__tablename__ = 'song'

	lyrics = db.Column(db.String(2000), nullable=False)
	language = db.Column(db.String(80), nullable=False)

	account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

	results = db.relationship("Words",
		secondary=song_result,
 		cascade='all, delete',
 		passive_deletes=True,
		backref=db.backref('songs', lazy=True)
	)


	def __init__(self, name, lyrics, language):
		self.name = name
		self.lyrics = lyrics
		self.language = language

