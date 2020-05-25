from application import db
from application import views
from application.models import Base

import datetime

from sqlalchemy import DateTime

class User(Base):

	__tablename__ = "account"

	date_created = db.Column(db.DateTime(), default=db.func.current_timestamp())

	name = db.Column(db.String(80), nullable=False)
	username = db.Column(db.String(80), nullable=False, unique=True)
	password = db.Column(db.String(80), nullable=False)
	admin = db.Column(db.Boolean, default=False, nullable=False)

	def __init__(self, name, username, password, admin):
		self.name = name
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

