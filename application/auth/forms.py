from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators

# Lomaketta kuvaava luokka.

class LoginForm(FlaskForm):
	username = StringField("Username", [validators.Length(min=1)])
	password = PasswordField("Password", [validators.Length(min=4)])
 
	class Meta:
		csrf = False

class CreateForm(FlaskForm):
	name = StringField("Full name", [validators.Length(min=1)])
	username = StringField("Username", [validators.Length(min=1)])
	password = PasswordField("Password", [validators.Length(min=4)])
 
	class Meta:
		csrf = False

class AuthForm(FlaskForm):
	name = StringField("Full name", [validators.Length(min=1)])
	username = StringField("Username", [validators.Length(min=1)])
	password = PasswordField("Password", [validators.Length(min=4)])
 
	class Meta:
		csrf = False
