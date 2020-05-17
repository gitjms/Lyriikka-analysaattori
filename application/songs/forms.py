from flask_wtf import FlaskForm
from wtforms import TextAreaField, validators

class SongForm(FlaskForm):
	title = TextAreaField("title", [validators.Length(min=1)])
	author = TextAreaField("author", [validators.Length(min=1)])
	lyrics = TextAreaField("lyrics", [validators.Length(min=1)])
 
	class Meta:
		csrf = False
