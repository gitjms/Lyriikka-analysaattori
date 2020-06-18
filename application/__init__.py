from flask import Flask
app = Flask(__name__)

import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db_uri = "sqlite:///songs.db"

if os.environ.get("HEROKU"):
	app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
	app.config["ENV"] = 'production'
else:
	app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
	app.config["SQLALCHEMY_ECHO"] = True
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
	app.config["ENV"] = 'development'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------
# login
#----------------------------------------------
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

app.static_folder = 'static'

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"


#----------------------------------------------
# roles in login_required
#----------------------------------------------
from functools import wraps
from flask_login import current_user

def login_required(_func=None, *, roles=[]):
	def wrapper(func):
		@wraps(func)
		def decorated_view(*args, **kwargs):
			if not (current_user and current_user.is_authenticated):
				return login_manager.unauthorized()

			if current_user.role not in roles:
				return login_manager.unauthorized()

			return func(*args, **kwargs)
		return decorated_view
	return wrapper if _func is None else wrapper(_func)


# load application content
from application import models
from application import views

from application.roles import models
 
from application.auth import models
from application.auth import views

from application.authors import models
from application.authors import views

from application.songs import models
from application.songs import views
 
from application.poets import models
from application.poets import views

from application.poems import models
from application.poems import views

from application.words import models
from application.words import views

from application.admin import views


#----------------------------------------------
# create admin and guest accounts
#----------------------------------------------
from application.roles.models import Role
from sqlalchemy.event import listen
from sqlalchemy import event, DDL

@event.listens_for(Role.__table__, 'after_create')
def insert_initial_roles(*args, **kwargs):
	db.session.add(Role(role='ADMIN'))
	db.session.commit()
	db.session.add(Role(role='GUEST'))
	db.session.commit()
	db.session.add(Role(role='USER'))
	db.session.commit()


from application.auth.models import User
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(user_id)


# database creation
db.create_all()
