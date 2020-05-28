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
					"	COUNT(Song.id),"
                    "	COUNT(Author.id),"
                    "	COUNT(Song.language),"
                    "	results.matches "
					"FROM Song "
					"JOIN author_song ON Song.id = author_song.song_id "
					"JOIN Author ON author_song.author_id = Author.id "
					"JOIN results ON results.song_id = Song.id;"
					)
		res = db.engine.execute(stmt)

		response = []
		for row in res:
			response.append({'songs':row[0], 'authors':row[1], 'languages':row[2], 'matches':row[3]})

		return response
