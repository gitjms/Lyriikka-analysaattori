from application import app, db
from application import views

from flask import g
from flask_login import current_user

from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import text

@app.before_request
def before_request():
	g.user = current_user

class Words(db.Model):

	__tablename__ = 'results'

	id = db.Column(db.Integer, primary_key=True)
	word = db.Column(db.String(), nullable=False)
	matches = db.Column(db.Integer, nullable=False)
	result_all = db.Column(JSON, nullable=False)
	result_no_stop_words = db.Column(JSON, nullable=False)

	def __init__(self, word, matches, result_all, result_no_stop_words):
		self.word = word
		self.matches = matches
		self.result_all = result_all
		self.result_no_stop_words = result_no_stop_words

	@staticmethod
	def find_words():

		if g.user.role == "GUEST" or g.user.role == "ADMIN":
			user_list = [1,2]
		else:
			user_list = [1,g.user.id]

		stmt1 = text("SELECT "
					"	DISTINCT results.word, "
                    "	COUNT(Song.id) AS w_count, "
					"	SUM(results.matches) "
					"FROM results "
					"JOIN song_result ON song_result.results_id = results.id "
					"JOIN Song ON Song.id = song_result.song_id "
					"JOIN account ON account.id = Song.account_id "
					"WHERE account.id IN (:user1,:user2) "
					"GROUP BY results.word "
					"ORDER BY SUM(results.matches) DESC "
					"LIMIT :limit").params(user1=user_list[0],user2=user_list[1], limit=5)
		res1 = db.engine.execute(stmt1)
		response1 = []
		for row in res1:
			response1.append({'word':row[0],'count':row[1]})

		return response1

	@staticmethod
	def find_stats():

		if g.user.role == "GUEST" or g.user.role == "ADMIN":
			user_list = [1,2]
		else:
			user_list = [1,g.user.id]

		stmt2 = text("SELECT "
                    "	co.matches, "
                    "	co.average, "
					"	results.word "
					"FROM results "
					"INNER JOIN ( "
					"	SELECT "
					"		DISTINCT results.word AS words, "
					"		SUM(results.matches) AS matches, "
					"		AVG(results.matches) AS average "
					"	FROM results "
					"	JOIN song_result ON song_result.results_id = results.id "
					"	JOIN Song ON Song.id = song_result.song_id "
					"	JOIN account ON account.id = Song.account_id "
					"	WHERE account.id IN (:user1,:user2) "
					"	GROUP BY results.word "
					"	ORDER BY matches DESC "
					") as co "
					"ON co.words = results.word "
					"GROUP BY co.matches, co.words, results.word, co.average "
					"ORDER BY co.matches DESC "
					"LIMIT :limit").params(user1=user_list[0],user2=user_list[1], limit=5)
		res2 = db.engine.execute(stmt2)
		response2 = []
		for row in res2:
			response2.append({'matches':row[0], 'average':row[1]})

		return response2
