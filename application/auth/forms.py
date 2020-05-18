from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators

# Lomaketta kuvaava luokka.

class LoginForm(FlaskForm):
	username = StringField("Username", [validators.Length(min=1)])
	password = PasswordField("Password", [validators.Length(min=1)])
 
	class Meta:
		csrf = False
