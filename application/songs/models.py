from application import db
from application import views
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

	@staticmethod
	def find_songs_authors_languages_matches():
		stmt = text("SELECT"
					"	DISTINCT Song.language,"
                    "	COUNT(DISTINCT Song.title),"
                    "	COUNT(DISTINCT Author.name) "
					"FROM Song "
					"LEFT JOIN author_song ON Song.id = author_song.song_id "
					"LEFT JOIN Author ON author_song.author_id = Author.id "
					"GROUP BY Song.language "
					"ORDER BY Song.language ASC;"
					)
		res = db.engine.execute(stmt)

		response = []
		for row in res:
			response.append({'languages':row[0], 'songs':row[1], 'authors':row[2]})

		return response
