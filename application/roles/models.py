from application import db


class Role(db.Model):

	__tablename__ = "roles"

	id = db.Column(db.Integer, primary_key=True)
	role = db.Column(db.String(255), nullable=False)

	user = db.relationship("User", backref='roles', lazy=True)

	def __init__(self, role):
		self.role = role

	def get_id(self):
		return self.id


