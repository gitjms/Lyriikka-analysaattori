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
	db.Column(	'results_id',							# right
				db.ForeignKey('results.id', ondelete='cascade'),
				primary_key=True)
)


class Song(Base):

	__tablename__ = 'song'

	lyrics = db.Column(db.Text, nullable=False)
	language = db.Column(db.String(255), nullable=False)

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


	@staticmethod
	def find_database_songs_status():

		if g.user.role == "GUEST" or g.user.role == "ADMIN":
			user_list = [1,2]
		else:
			user_list = [1,g.user.id]

		stmt = text("SELECT DISTINCT Song.language, "
					"	COUNT(DISTINCT Song.name), "
					"	COUNT(DISTINCT Author.name) "
					"FROM Song "
					"LEFT JOIN author_song ON Song.id = author_song.song_id "
					"LEFT JOIN Author ON author_song.author_id = Author.id "
					"LEFT JOIN account ON account.id = Song.account_id "
					"WHERE account.id IN (:user1,:user2) "
					"GROUP BY Song.language "
					"ORDER BY Song.language ASC").params(user1=user_list[0],user2=user_list[1])

		result = db.engine.execute(stmt)

		response = []
		for row in result:
			response.append({'languages':row[0], 'songs':row[1], 'authors':row[2]})

		return response

