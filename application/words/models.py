from application import db
from application import views

from sqlalchemy.dialects.postgresql import JSON


class Words(db.Model):

	__tablename__ = 'results'

	id = db.Column(db.Integer, primary_key=True)
	word = db.Column(db.String())
	result_all = db.Column(JSON)
	result_no_stop_words = db.Column(JSON)

	# song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)

	def __init__(self, word, result_all, result_no_stop_words):
		self.word = word
		self.result_all = result_all
		self.result_no_stop_words = result_no_stop_words
