from application import app, db
from application import views
from application.models import Base

import os

from flask import g
from flask_login import current_user

from sqlalchemy.sql import text


@app.before_request
def before_request():
	g.user = current_user


# join table AUTHOR_SONG
author_song = db.Table('author_song', Base.metadata,
	db.Column(	'author_id',						# left
				db.ForeignKey('author.id', ondelete='cascade'),
				primary_key=True),
	db.Column(	'song_id',							# right
				db.ForeignKey('song.id', ondelete='cascade'),
				primary_key=True)
)

class Author(Base):

	__tablename__ = 'author'


	songs = db.relationship("Song",
		secondary=author_song,
 		cascade='all, delete',
 		passive_deletes=True,
		backref=db.backref('authors', lazy=True)
	)


	def __init__(self, name):
		self.name = name

	def get_id(self):
		return self.id

	@staticmethod
	def find_authors():

		if g.user.role == "GUEST" or g.user.role == "ADMIN":
			user_list = [1,2]
		else:
			user_list = [1,g.user.id]

		if os.environ.get("HEROKU"):
			song_group = "STRING_AGG (Song.name,'; ') songs, "
		else:
			song_group = "GROUP_CONCAT (Song.name,'; ') songs, "

		stmt = text("SELECT "
					"	DISTINCT author.name, "
					+ song_group +
					"	Song.language, "
					"	author.id "
					"FROM Song "
					"INNER JOIN author_song ON author_song.song_id = Song.id "
					"INNER JOIN author ON author.id = author_song.author_id "
					"JOIN account ON account.id = Song.account_id "
					"WHERE account.id IN (:user1,:user2) "
					"GROUP BY author.name, Song.language, author.id "
					"ORDER BY Song.language, author.name ASC").params(user1=user_list[0],user2=user_list[1])
		res = db.engine.execute(stmt)
		response = []
		for row in res:
			response.append({'author':row[0],'songs':row[1],'language':row[2],'id':row[3]})

		return response
