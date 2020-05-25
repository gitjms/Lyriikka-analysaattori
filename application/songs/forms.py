from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, validators
from wtforms.validators import DataRequired

# Lomaketta kuvaava luokka.

class SongForm(FlaskForm):
	title = TextAreaField("title", [validators.Length(min=1)])
	lyrics = TextAreaField("lyrics", [validators.Length(min=1)])
	language = SelectField('language', [validators.DataRequired()],choices=[('',''), ('finnish','finnish'), ('english','english'), ('french','french')])
	author = TextAreaField("author", [validators.Length(min=1)])
 
	class Meta:
		csrf = False