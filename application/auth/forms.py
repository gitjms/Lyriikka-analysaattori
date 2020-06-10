from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
from wtforms.validators import DataRequired

# Lomaketta kuvaava luokka.

class LoginForm(FlaskForm):
	username = StringField("Username", [validators.Length(min=1,max=25)])
	password = PasswordField("Password", [validators.Length(min=4,max=10)]
	)

	class Meta:
		csrf = False

class CreateUserForm(FlaskForm):
	name = StringField("Full name", [validators.Length(min=1,max=200),
			validators.DataRequired(),])
	username = StringField("Username", [validators.Length(min=1,max=25),
			validators.DataRequired(),])
	password = PasswordField("Password", [validators.Length(min=4,max=10),
			validators.DataRequired(),
			validators.EqualTo('confirm', message='Passwords must match')]
	)
	confirm = PasswordField('Repeat Password')
 
	class Meta:
		csrf = False
