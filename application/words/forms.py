from flask_wtf import FlaskForm
from wtforms import TextAreaField, validators

# Lomaketta kuvaava luokka.

class WordForm(FlaskForm):
	word = TextAreaField("word", [validators.Length(min=1)])
 
	class Meta:
		csrf = False
