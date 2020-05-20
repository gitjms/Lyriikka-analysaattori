from flask import redirect, url_for, render_template, request, flash, g
from flask_wtf import FlaskForm
from flask_login import login_required, current_user

import operator
import re
import nltk
from collections import Counter

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from application import app, db
from application.songs.models import Song
from application.words.models import Words
from application.words.forms import WordForm
#-------------------------------------
# STOPWORDS FROM CATALOGUES
# from nltk.corpus import stopwords
#-------------------------------------
# OWN STOPWORDS
from application.stopwords.stopwords import stops

# Lomakkeen näyttämisen ja lähetyksen vastaanottava toiminnallisuus.

@app.before_request
def before_request():
	g.user = current_user


#-----------------------------------------
#		SHOW: words_find()
#-----------------------------------------
@app.route("/words/show/", methods=["GET", "POST"])
@login_required
def words_find():
	errors = []
	results = {}

	song_list = [g.user.id,1]
	form = WordForm(request.form)
	word_to_find = request.form['wordsearch']

	# text processing
	nltk.data.path.append('C:/nltk_data/')
	raw_list = db.session().query(Song.lyrics).filter(Song.account_id.in_((song_list))).all()

	raw = ' '.join([str(elem) for elem in raw_list]).rstrip('\n')

	tokens = nltk.word_tokenize(raw)
	text = nltk.Text(tokens)

	# remove punctuation, count raw words
	nonPunct = re.compile('.*[A-Za-z].*')
	raw_words = [w for w in text if nonPunct.match(w)]
	raw_word_count = Counter(raw_words)

	# stop words
	# from catalogues:
	# stops = stopwords.stopwords.stops#stopwords.words('english')
	# from own file:
	no_stop_words = [w for w in raw_words if w.lower() not in stops]
	no_stop_words_count = Counter(no_stop_words)
	# save the results
	results = sorted(
		no_stop_words_count.items(),
		key=operator.itemgetter(1),
		reverse=True
	)[:10]

	try:
		result = Words(
			word = word_to_find,
			result_all=raw_word_count,
			result_no_stop_words=no_stop_words_count
		)
		db.session.add(result)
		db.session.commit()
	except:
		flash("Unable to add item to Words database.", "danger")
		errors.append("Unable to add item to database.")

	if request.method == "GET":
		return render_template("words/words.html", form = form)

	if request.form.get("Back") == "Back":
		return redirect(url_for("songs_index"))

	return render_template("words/words.html", songs = Song.query.filter(Song.account_id.in_((song_list))), word=word_to_find, errors=errors, results=results)


