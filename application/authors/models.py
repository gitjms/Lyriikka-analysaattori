from application import db
from application import views
from application.models import Base


author_song = db.Table('author_song', Base.metadata,
			db.Column(	'author_id',					# left
						db.Integer,
						db.ForeignKey('author.id'),
						primary_key=True),
			db.Column(	'song_id',						# right
						db.Integer,
						db.ForeignKey('song.id'),
						primary_key=True)
)

class Author(Base):

	__tablename__ = 'author'

	name = db.Column(db.String(80), nullable=False)

	# right:
	author_song = db.relationship("Song",
		secondary=author_song,
		# primaryjoin="author.id==author_song.author_id",
		# secondaryjoin="song.id==author_song.song_id",
		backref=db.backref('authors', lazy=True))#,#'author',								# left
		# lazy=True)

	# __table_args__ = {'extend_existing': True}

	def __init__(self, name):
		self.name = name
  
	def get_id(self):
		return self.id

