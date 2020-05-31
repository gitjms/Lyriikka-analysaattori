from application import db
from application import views

from flask import g

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
		user_list = [g.user.id,1]

		stmt = text("SELECT "
					"	DISTINCT results.word, "
                    "	results.matches, "
                    "	COUNT(results.matches), "
                    "	SUM(results.matches), "
                    "	AVG(results.matches) "
					"FROM results "
					"JOIN Song ON results.song_id = Song.id "
					"JOIN account ON account.id = Song.account_id "
					"WHERE account.id IN (:user1,:user2) "
					"GROUP BY results.word, results.matches "
					"ORDER BY results.matches DESC "
					"LIMIT :limit").params(user1=user_list[0],user2=user_list[1],limit=5)
		res = db.engine.execute(stmt)
		response = []
		for row in res:
			response.append({'word':row[0], 'totcount':row[1], 'count':row[2], 'sum':row[3], 'average':row[4]})

		return response
