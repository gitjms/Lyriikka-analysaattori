from application import app, db
from application.models import Base

import os

from flask import g
from flask_login import current_user

from sqlalchemy.dialects.postgresql import JSON
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

	result_all = db.Column(JSON, nullable=True)
	result_no_stop_words = db.Column(JSON, nullable=True)

	songs = db.relationship("Song",
		secondary=author_song,
 		cascade='all, delete',
 		passive_deletes=True,
		backref=db.backref('authors', lazy=True)
	)


	def __init__(self, name, result_all, result_no_stop_words):
		self.name = name
		self.result_all = result_all
		self.result_no_stop_words = result_no_stop_words

	def get_id(self):
		return self.id


	@staticmethod
	def get_authors(language):

		if os.environ.get("HEROKU"):
			song_group = "STRING_AGG (Song.name,'; ') songs, "
		else:
			song_group = "GROUP_CONCAT (Song.name,'; ') songs, "

		if language == "":
			lang = ""
		else:
			lang = "AND Song.language = '" + language + "' "

		stmt = text("SELECT "
					"	DISTINCT author.name, "
					+ song_group +
					"	Song.language, "
					"	author.id "
					"FROM Song "
					"INNER JOIN author_song ON author_song.song_id = Song.id "
					"INNER JOIN author ON author.id = author_song.author_id "
					"JOIN account ON account.id = Song.account_id "
					"AND account.role_id = Song.account_role "
					"WHERE account_id = :userid "
					"OR account_role = :accrole "
					+ lang +
					"GROUP BY author.name, Song.language, author.id "
					"ORDER BY Song.language, author.name ASC").params(userid=g.user.id,accrole=1)
		res = db.engine.execute(stmt)
		response = []
		for row in res:
			response.append({'author':row[0],'songs':row[1],'language':row[2],'id':row[3]})

		return response


	@staticmethod
	def get_authorsongs(author_id):

		stmt = text("SELECT Song.id, "
					"		Song.lyrics, "
					"		Song.name, "
					"		Song.language "
					"FROM Song "
					"LEFT JOIN author_song ON Song.id = author_song.song_id "
					"LEFT JOIN Author ON author_song.author_id = Author.id "
					"LEFT JOIN account ON account.id = Song.account_id "
					"AND account.role_id = Song.account_role "
					"WHERE account_id = :userid "
					"OR account_role = :accrole "
					"AND author.id = :id "
					"GROUP BY Song.id, Song.lyrics, Song.name, Song.language").params(userid=g.user.id,accrole=1,id=author_id)

		result = db.engine.execute(stmt)

		response = []
		for row in result:
			response.append({'id':row[0],'lyrics':row[1],'title':row[2],'language':row[3]})

		return response

