from flask_wtf import FlaskForm
from wtforms import StringField

class SongForm(FlaskForm):
    name = StringField("Song name")
 
    class Meta:
        csrf = False
