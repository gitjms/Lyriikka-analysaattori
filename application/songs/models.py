from application import db

from application import views


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(144), nullable=False)
    text = db.Column(db.String(1000), nullable=False)

    def __init__(self, name, text):
        self.name = name
        self.text = text
		