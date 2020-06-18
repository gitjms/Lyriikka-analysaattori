from application import db
from application import views
from application.models import Base

import datetime

from sqlalchemy import DateTime

class User(Base):

	__tablename__ = "account"

	username = db.Column(db.String(255), nullable=False, unique=True)
	password = db.Column(db.String(255), nullable=False)

	role = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False, primary_key=True)

	date_created = db.Column(db.DateTime(), default=db.func.current_timestamp())

	def __init__(self, name, username, password):
		self.name = name
		self.username = username
		self.password = password

	def get_id(self):
		return self.id

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def is_authenticated(self):
		return True
