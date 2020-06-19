from application import app, db

from flask import g
from flask_login import current_user

from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import text

@app.before_request
def before_request():
	g.user = current_user

class Word(db.Model):

	__tablename__ = 'result'

	id = db.Column(db.Integer, primary_key=True)
	word = db.Column(db.String(255), nullable=False)
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

		stmt1 = text("SELECT "
					"	DISTINCT result.word, "
                    "	COUNT(Song.id) AS w_count, "
					"	SUM(result.matches) "
					"FROM result "
					"JOIN song_result ON song_result.result_id = result.id "
					"JOIN Song ON Song.id = song_result.song_id "
					"JOIN account ON account.id = Song.account_id "
					"AND account.role_id = Song.account_role "
					"WHERE account_id = :userid OR account_role = :accrole "
					"GROUP BY result.word "
					"ORDER BY SUM(result.matches) DESC "
					"LIMIT :limit").params(userid=g.user.id,accrole=1, limit=5)
		res1 = db.engine.execute(stmt1)
		response1 = []
		for row in res1:
			response1.append({'word':row[0],'count':row[1]})

		return response1

	@staticmethod
	def find_stats():

		stmt2 = text("SELECT "
                    "	co.matches, "
                    "	co.average, "
					"	result.word "
					"FROM result "
					"INNER JOIN ( "
					"	SELECT "
					"		DISTINCT result.word AS words, "
					"		SUM(result.matches) AS matches, "
					"		ROUND( AVG(result.matches), 1 ) AS average "
					"	FROM result "
					"	JOIN song_result ON song_result.result_id = result.id "
					"	JOIN Song ON Song.id = song_result.song_id "
					"	JOIN account ON account.id = Song.account_id "
					"	AND account.role_id = Song.account_role "
					"	WHERE account_id = :userid OR account_role = :accrole "
					"	GROUP BY result.word "
					"	ORDER BY matches DESC "
					") as co "
					"ON co.words = result.word "
					"GROUP BY co.matches, co.words, result.word, co.average "
					"ORDER BY co.matches DESC "
					"LIMIT :limit").params(userid=g.user.id,accrole=1, limit=5)
		res2 = db.engine.execute(stmt2)
		response2 = []
		for row in res2:
			response2.append({'matches':row[0], 'average':row[1]})

		return response2
