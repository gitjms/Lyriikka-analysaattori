from application import db


class Role(db.Model):

	__tablename__ = "roles"

	id = db.Column(db.Integer, primary_key=True)
	role = db.Column(db.String(255), primary_key=True)


	def __init__(self, id, role):
		self.id = id
		self.role = role

	def get_id(self):
		return self.id

	def get_role(self):
		return self.role


