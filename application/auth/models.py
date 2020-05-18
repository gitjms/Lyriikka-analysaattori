from application import db

from application import views


class User(db.Model):

	__tablename__ = "account"

	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),onupdate=db.func.current_timestamp())
	fullname = db.Column(db.String(144), nullable=False)
	username = db.Column(db.String(144), nullable=False)
	password = db.Column(db.String(144), nullable=False)
	admin = db.Column(db.Boolean, default=False, nullable=False)

	def __init__(self, fullname, username, password, admin):
		self.fullname = fullname
		self.username = username
		self.password = password
		self.admin = admin

	def get_id(self):
		return self.id

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def is_authenticated(self):
		return True
