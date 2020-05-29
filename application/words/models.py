from application import db
from application import views

from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import text

class Words(db.Model):

	__tablename__ = 'results'

	id = db.Column(db.Integer, primary_key=True)
	word = db.Column(db.String(), nullable=False)
	matches = db.Column(db.Integer, nullable=False)
	result_all = db.Column(JSON, nullable=False)
	result_no_stop_words = db.Column(JSON, nullable=False)

	song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)

	def __init__(self, word, matches, result_all, result_no_stop_words):
		self.word = word
		self.matches = matches
		self.result_all = result_all
		self.result_no_stop_words = result_no_stop_words

	@staticmethod
	def find_songs_authors_with_matches_geq_avg():
		stmt = text("SELECT"
					"	results.word,"
                    "	Author.name,"
                    "	Song.title,"
                    "	results.matches,"
                    "	SUM(results.matches) AS sum, "
                    "	AVG(results.matches) AS avg "
					"FROM account "
					"JOIN Song ON account.id = Song.account_id "
					"JOIN results ON Song.id = results.song_id "
					"JOIN author_song ON Song.id = author_song.song_id "
					"JOIN Author ON author_song.author_id = Author.id "
					"GROUP BY results.word, Author.name "
					"ORDER BY results.matches DESC;"
					)
		res = db.engine.execute(stmt)

		response = []
		for row in res:
			response.append({'word':row[0], 'author':row[1], 'title':row[2], 'matches':row[3], 'sum':row[4], 'average':row[5]})

		return response

