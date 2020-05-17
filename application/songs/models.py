from application import db

from application import views


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(144), nullable=False)
    author = db.Column(db.String(144), nullable=False)
    lyrics = db.Column(db.String(2000), nullable=False)

    def __init__(self, title, author, lyrics):
        self.title = title
        self.author = author
        self.lyrics = lyrics
		