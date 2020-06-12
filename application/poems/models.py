from application import app, db
from application.models import Base

import os

from flask import g
from flask_login import current_user

from sqlalchemy.sql import text


@app.before_request
def before_request():
	g.user = current_user


class Poem(Base):

	__tablename__ = 'poem'

	lyrics = db.Column(db.Text, nullable=False)
	language = db.Column(db.String(255), nullable=False)

	account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)


	def __init__(self, name, lyrics, language):
		self.name = name
		self.lyrics = lyrics
		self.language = language


	@staticmethod
	def find_database_poems_status():

		if g.user.role == "GUEST" or g.user.role == "ADMIN":
			user_list = [1,2]
		else:
			user_list = [1,g.user.id]

		stmt = text("SELECT DISTINCT Poem.language, "
					"	COUNT(DISTINCT Poem.name), "
					"	COUNT(DISTINCT Poet.name) "
					"FROM Poem "
					"LEFT JOIN poet_poem ON Poem.id = poet_poem.poem_id "
					"LEFT JOIN Poet ON poet_poem.poet_id = Poet.id "
					"LEFT JOIN account ON account.id = Poem.account_id "
					"WHERE account.id IN (:user1,:user2) "
					"GROUP BY Poem.language "
					"ORDER BY Poem.language ASC").params(user1=user_list[0],user2=user_list[1])

		result = db.engine.execute(stmt)

		response = []
		for row in result:
			response.append({'languages':row[0], 'poems':row[1], 'poets':row[2]})

		return response

