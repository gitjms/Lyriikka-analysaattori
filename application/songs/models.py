from application import db
from application import views
from application import app
from flask import g
from flask_login import current_user
from sqlalchemy.sql import text


class Song(db.Model):

	__tablename__ = 'song'

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80), nullable=False, unique=True)
	lyrics = db.Column(db.String(2000), nullable=False)
	language = db.Column(db.String(80), nullable=False)

	account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)


	def __init__(self, title, lyrics, language):
		self.title = title
		self.lyrics = lyrics
		self.language = language


	@app.before_request
	def before_request():
		g.user = current_user


	@staticmethod
	def find_songs_authors_languages_matches():

		user_1 = 1
		user_2 = g.user.id
		
		stmt = text("SELECT"
					"	DISTINCT Song.language,"
                    "	COUNT(DISTINCT Song.title),"
                    "	COUNT(DISTINCT Author.name) "
					"FROM Song "
					"LEFT JOIN author_song ON Song.id = author_song.song_id "
					"LEFT JOIN Author ON author_song.author_id = Author.id "
					"LEFT JOIN account ON Song.account_id = account.id "
					"WHERE account.id IN (:user_1, :user_2) "
					"GROUP BY Song.language "
					"ORDER BY Song.language ASC;"
					).params(user1=user_1,user2=user_2)

		res = db.engine.execute(stmt)

		response = []
		for row in res:
			response.append({'languages':row[0], 'songs':row[1], 'authors':row[2]})

		return response
