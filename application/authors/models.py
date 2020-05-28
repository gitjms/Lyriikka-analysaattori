from application import db
from application import views
from application.models import Base


# join table AUTHOR_SONG
author_song = db.Table('author_song', Base.metadata,
	db.Column(	'author_id',						# left
				db.ForeignKey('author.id', ondelete='cascade'),
				primary_key=True),
	db.Column(	'song_id',							# right
				db.ForeignKey('song.id', ondelete='cascade'),
				primary_key=True)
)

class Author(Base):

	__tablename__ = 'author'

	name = db.Column(db.String(80), nullable=False)

	songs = db.relationship("Song",
		cascade='all, delete',
		secondary=author_song,
		passive_deletes=True,
		backref=db.backref('authors', lazy=True),
		lazy='subquery'
	)


	def __init__(self, name):
		self.name = name

	def get_id(self):
		return self.id
