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
	account_id = db.Column(db.Integer, nullable=False)
	account_role = db.Column(db.Integer, nullable=False)


	def __init__(self, name, lyrics, language, account_id, account_role):
		self.name = name
		self.lyrics = lyrics
		self.language = language
		self.account_id = account_id
		self.account_role = account_role


	@staticmethod
	def find_database_poems_status():

		stmt = text("SELECT DISTINCT Poem.language, "
					"	COUNT(DISTINCT Poem.name), "
					"	COUNT(DISTINCT Poet.name) "
					"FROM Poem "
					"LEFT JOIN poet_poem ON Poem.id = poet_poem.poem_id "
					"LEFT JOIN Poet ON poet_poem.poet_id = Poet.id "
					"LEFT JOIN account ON account.id = Poem.account_id "
					"AND account.role_id = Poem.account_role "
					"WHERE account_id = :userid "
					"OR account_role = :accrole "
					"GROUP BY Poem.language "
					"ORDER BY Poem.language ASC").params(userid=g.user.id,accrole=1)

		result = db.engine.execute(stmt)

		response = []
		for row in result:
			response.append({'languages':row[0], 'poems':row[1], 'poets':row[2]})

		return response

