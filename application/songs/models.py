from application import db

from application import views


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(144), nullable=False)
    author = db.Column(db.String(144), nullable=False)
    text = db.Column(db.String(2000), nullable=False)

    def __init__(self, name, author, text):
        self.name = name
        self.author = author
        self.text = text
		