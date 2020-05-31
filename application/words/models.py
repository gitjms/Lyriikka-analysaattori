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
                    "	COUNT(song.sum), "
                    "	results.matches/COUNT(song.sum) "
					"FROM results "
					"INNER JOIN "
					"( "
					"	SELECT "
					"		DISTINCT Song.account_id, "
					"		results.matches AS matches, "
					"		SUM(results.matches) AS sum "
					"	FROM song "
					"	JOIN account ON account.id = Song.account_id "
					"	JOIN results ON results.song_id = Song.id "
					"	WHERE account.id IN (:user1,:user2) "
					") AS song "
					"GROUP BY results.word "
					"ORDER BY results.matches DESC "
					"LIMIT :limit").params(user1=user_list[0],user2=user_list[1],limit=5)
		res = db.engine.execute(stmt)
		response = []
		for row in res:
			response.append({'word':row[0], 'totcount':row[1], 'numsongs':row[2], 'average':row[3]})

		return response
