from application import db

class Base(db.Model):

	__abstract__ = True
  
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(), nullable=False)
