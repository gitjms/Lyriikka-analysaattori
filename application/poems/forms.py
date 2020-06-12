from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, validators
from wtforms.validators import DataRequired


class NewPoemForm(FlaskForm):
	title = TextAreaField("title", [validators.Length(min=1,max=250)])
	lyrics = TextAreaField("lyrics", [validators.Length(min=1)])
	language = SelectField('language', [validators.DataRequired()],choices=[('',''), ('finnish','finnish'), ('english','english'), ('french','french')])
	poet = TextAreaField("poet", [validators.Length(min=1,max=250)])
 
	class Meta:
		csrf = False

class EditPoemForm(FlaskForm):
	title = TextAreaField("title", [validators.Length(min=1,max=250)])
	lyrics = TextAreaField("lyrics", [validators.Length(min=1)])
	language = SelectField('language', [validators.DataRequired()],choices=[('finnish','finnish'), ('english','english'), ('french','french')])
	poet = TextAreaField("poet", [validators.Length(min=1,max=250)])
 
	class Meta:
		csrf = False