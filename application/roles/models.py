from application import db


class Role(db.Model):

	__tablename__ = "roles"

	id = db.Column(db.Integer, primary_key=True)
	role = db.Column(db.String(255), nullable=False)

	account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

	def __init__(self, role):
		self.role = role

	def get_id(self):
		return self.id


