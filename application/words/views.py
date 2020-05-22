from flask import redirect, url_for, render_template, request, flash, g, Markup
from flask_wtf import FlaskForm
from flask_login import login_required, current_user

import json

import operator
import re
import nltk
from collections import Counter
# from flask import jsonify

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from application import app, db
from application.songs.models import Song
from application.words.models import Words
from application.words.forms import WordForm
# STOPWORDS FROM CATALOGUES:
# from nltk.corpus import stopwords
# OWN STOPWORDS:
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

	user_list = [g.user.id,1]
	form = WordForm(request.form)
	word_to_find = request.form['wordsearch']

	# text processing
	nltk.data.path.append('./nltk_data/')
	qry_list = db.session().query(Song.id,Song.lyrics,Song.title).filter(Song.account_id.in_((user_list))).all()
	song_list = []
	for i in qry_list:
		raw_to_string = ' '.join([str(elem) for elem in i])
		song_list.append([i[0], replace_chars(raw_to_string),i[2]])

	text_list = [] # [ song_id, lyrics, song_title ]
	for song in song_list:
		tokens = nltk.word_tokenize(song[1])
		text_list.append([song[0], nltk.Text(tokens), song[2]])

	# remove punctuation, count raw words
	raw_word_count = [] # Counter(raw_words)
	raw_words_list = [] # [ song_id, raw_words ]
	for txt in text_list: # [ song_id, lyrics ]
		count = 0
		raw_words = []
		nonPunct = re.compile('.*[A-Za-z].*')
		for i in txt[1]:
			if nonPunct.match(i):
				raw_words.append(i)
			if i.lower() == word_to_find.lower():
				count += 1
		if count > 0:
			raw_words_list.append([txt[0], raw_words, txt[2]])
			raw_word_count.append(Counter(raw_words))

	# markup search word matches in source text
	new_songlist = [] # [ song_id, Markup(new_string) ]
	new_raw_words_list = []
	tot_count = 0
	for item in raw_words_list: # [ song_id, raw_words, song_title ]
		w_list = []             # item[0]=song_id
		count = 0               # item[1]=raw_words
		for w in item[1]:       # item[2]=song_title
			if w.lower() == word_to_find.lower():
				w = r"<mark><strong>"+w+"</strong></mark>"
				count += 1
				tot_count += 1
			w_list.append(w)
		if count > 0:
			new_string = ' '.join(w_list)
			new_songlist.append([item[0],Markup(new_string),item[2]])
			new_raw_words_list.append([count, [item[0], w_list]])

	# stop words
	# from catalogues:
	# stops = stopwords.words('english')#('finnish')
	no_stop_words_list = []
	results_list = []
	results = {}
	graph_list = []
	for words_list in new_raw_words_list: # [count, [song_id, raw_words] ]
		no_stop_words = [Markup(w.lower()) for w in words_list[1][1] if w.lower() not in stops]
		no_stop_words_count = Counter(no_stop_words)
		graph_list.append(no_stop_words)
		no_stop_words_list.append([words_list[1][0], no_stop_words_count])
		# save the results
		results = sorted(
			no_stop_words_count.items(),
			key=operator.itemgetter(1),
			reverse=True
		)[:10]
		# results_list = [ song_id, Word, Count ]
		results_list.append([words_list[1][0], results, words_list[0]])

	# store to database
	page_results = None
	page_songs = None
	result_set = []
	result_set.append([raw_word_count, no_stop_words_list])
	if tot_count > 0:
		page_results = results_list
		page_songs = new_songlist
		
		# data for graph
		values = []
		result_values = {}
		labels = []
		for item in graph_list:
			for i in item:
				if (i.find('<mark><strong>') != -1):
					j = word_to_find
					values.append(j)
				else:
					values.append(i)
		values_count = Counter(values)
		result_values = sorted(
			values_count.items(),
			key=operator.itemgetter(1),
			reverse=True
		)[:10]

		for i in range(len(raw_word_count)):
			try:
				result = Words(
					word = word_to_find,
					result_all=raw_word_count[i],
					result_no_stop_words=no_stop_words_list[i][1]
				)
				result.song_id = no_stop_words_list[i][0]
				result.user_id = g.user.id
				db.session.add(result)
				db.session.commit()
			except SQLAlchemyError:
				db.session.rollback()
				flash("Unable to add item to Words database.", "danger")
				errors.append("Unable to add item to Words database.")
				break

	return render_template("words/words.html", frequencies = page_results, songs=page_songs, word=word_to_find, errors=errors, count = tot_count, song_count=len(new_songlist), graph_data=result_values)


def replace_chars(text):
	for ch in ['\\n','BRIDGE','POST-CHORUS','CHORUS','VERSE','V1','V2','V3','V4','V5','V6','V7','V8','V9','V10','B1','B2','B3','B4','B5','B6','B7','B8','B9','B10','C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','\'n','\n','\'n\'n','\'r','\'r\'n']:
		if ch in text:
			text = text.replace(ch,"")
	return text
