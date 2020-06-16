from application import app, db
from application.models import Base

import os

from flask import g
from flask_login import current_user

from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import text


@app.before_request
def before_request():
	g.user = current_user


# join table AUTHOR_SONG
poet_poem = db.Table('poet_poem', Base.metadata,
	db.Column(	'poet_id',							# left
				db.ForeignKey('poet.id', ondelete='cascade'),
				primary_key=True),
	db.Column(	'poem_id',							# right
				db.ForeignKey('poem.id', ondelete='cascade'),
				primary_key=True)
)


class Poet(Base):

	__tablename__ = 'poet'

	result_all = db.Column(JSON, nullable=True)
	result_no_stop_words = db.Column(JSON, nullable=True)

	poems = db.relationship("Poem",
		secondary=poet_poem,
 		cascade='all, delete',
 		passive_deletes=True,
		backref=db.backref('poets', lazy=True)
	)


	def __init__(self, name, result_all, result_no_stop_words):
		self.name = name
		self.result_all = result_all
		self.result_no_stop_words = result_no_stop_words


	@staticmethod
	def get_poets(language):

		if os.environ.get("HEROKU"):
			song_group = "STRING_AGG (Poem.name,'; ') poems, "
		else:
			song_group = "GROUP_CONCAT (Poem.name,'; ') poems, "

		if language == "":
			lang = ""
		else:
			lang = "AND Poem.language = '" + language + "' "

		stmt = text("SELECT "
					"	DISTINCT poet.name, "
					+ song_group +
					"	Poem.language, "
					"	Poet.id "
					"FROM Poet "
					"INNER JOIN poet_poem ON poet_poem.poet_id = Poet.id "
					"INNER JOIN Poem ON Poem.id = poet_poem.poem_id "
					"JOIN account ON account.id = Poem.account_id "
					"WHERE account_id = :userid OR account_role = :accrole " + lang +
					"GROUP BY Poet.name, Poem.language, Poet.id "
					"ORDER BY Poem.language, Poet.name ASC").params(userid=g.user.id,accrole=1)
		res = db.engine.execute(stmt)
		response = []
		for row in res:
			response.append({'poet':row[0],'poems':row[1],'language':row[2],'id':row[3]})

		return response


	@staticmethod
	def get_poetpoems(poet_id):

		stmt = text("SELECT Poem.id, "
					"		Poem.lyrics, "
					"		Poem.name, "
					"		Poem.language "
					"FROM Poem "
					"LEFT JOIN poet_poem ON Poem.id = poet_poem.poem_id "
					"LEFT JOIN Poet ON poet_poem.poet_id = Poet.id "
					"LEFT JOIN account ON account.id = Poem.account_id "
					"WHERE account_id = :userid OR account_role = :accrole AND Poet.id = :id "
					"GROUP BY Poem.id, Poem.lyrics, Poem.name, Poem.language").params(userid=g.user.id,accrole=1,id=poet_id)

		result = db.engine.execute(stmt)

		response = []
		for row in result:
			response.append({'id':row[0],'lyrics':row[1],'title':row[2],'language':row[3]})

		return response

