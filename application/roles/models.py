from application import db
from application import views


class Role(db.Model):

	__tablename__ = "roles"

	id = db.Column(db.Integer, primary_key=True)
	role = db.Column(db.String(80), nullable=False, unique=True)


	def __init__(self, role):
		self.role = role

	def get_id(self):
		return self.id


