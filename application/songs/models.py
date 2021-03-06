from application import app, db
from application.models import Base

import os

from flask import g
from flask_login import current_user

from sqlalchemy.sql import text


@app.before_request
def before_request():
	g.user = current_user


# join table SONG_RESULTS
song_result = db.Table('song_result', Base.metadata,
	db.Column(	'song_id',								# left
				db.ForeignKey('song.id', ondelete='cascade'),
				primary_key=True),
	db.Column(	'result_id',							# right
				db.ForeignKey('result.id', ondelete='cascade'),
				primary_key=True)
)


class Song(Base):

	__tablename__ = 'song'

	lyrics = db.Column(db.Text, nullable=False)
	language = db.Column(db.String(255), nullable=False)
	account_id = db.Column(db.Integer, nullable=False)
	account_role = db.Column(db.Integer, nullable=False)

	results = db.relationship("Word",
		secondary=song_result,
 		cascade='all, delete',
 		passive_deletes=True,
		backref=db.backref('songs', lazy=True)
	)


	def __init__(self, name, lyrics, language, account_id, account_role):
		self.name = name
		self.lyrics = lyrics
		self.language = language
		self.account_id = account_id
		self.account_role = account_role


	@staticmethod
	def find_database_songs_status():

		stmt = text("SELECT DISTINCT Song.language, "
					"	COUNT(DISTINCT Song.name), "
					"	COUNT(DISTINCT Author.name) "
					"FROM Song "
					"LEFT JOIN author_song ON Song.id = author_song.song_id "
					"LEFT JOIN Author ON author_song.author_id = Author.id "
					"LEFT JOIN account ON account.id = Song.account_id "
					"AND account.role_id = Song.account_role "
					"WHERE account_id = :userid "
					"OR account_role = :accrole "
					"GROUP BY Song.language "
					"ORDER BY Song.language ASC").params(userid=g.user.id,accrole=1)

		result = db.engine.execute(stmt)

		response = []
		for row in result:
			response.append({'languages':row[0], 'songs':row[1], 'authors':row[2]})

		return response

