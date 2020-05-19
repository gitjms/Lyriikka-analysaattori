from application import db
from application import views


class Words(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	words = db.Column(db.String(2000), nullable=False)

	song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)

	def __init__(self, words):
		self.words = words
