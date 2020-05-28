from flask import flash, g, Markup

import os
import operator
import re
import nltk
from nltk.corpus import stopwords
from collections import Counter

from application import db
from application.words.models import Words

from sqlalchemy.exc import IntegrityError, SQLAlchemyError


# raw words count
def proc_text(song_list, word_to_find):

	text_list = [] # [ song_id, lyrics, song_title ]
	nltk.data.path.append(os.getcwd()+'/application/nltk_data/')

	for song in song_list:
		tokens = nltk.word_tokenize(song[1])
		text_list.append([song[0], nltk.Text(tokens), song[2]])

	# remove punctuation, count raw words
	raw_word_count = [] # [ Counter(raw_words) ]
	raw_words_list = [] # [ song_id, raw_words ]
	for txt in text_list: # [ song_id, lyrics, song_title ]
		count = 0
		raw_words = []
		song_id = txt[0]
		lyrics = txt[1]
		song_title = txt[2]
		nonPunct = re.compile('.*[A-Za-z].*')
		for i in lyrics:
			if nonPunct.match(i):
				raw_words.append(i)
			if i.lower() == word_to_find.lower():
				count += 1
		if count > 0:
			raw_words_list.append([song_id, raw_words, song_title])
			raw_word_count.append(Counter(raw_words))

	# count matches and store source text without newlines
	new_songlist = [] # [ song_id, new_string ]
	new_raw_words_list = []
	tot_count = 0
	for item in raw_words_list: # [ song_id, raw_words, song_title ]
		w_list = []
		count = 0
		song_id = item[0]
		raw_words = item[1]
		song_title = item[2]
		for w in raw_words:
			if w.lower() == word_to_find.lower():
				count += 1
				tot_count += 1
			w_list.append(w)
		if count > 0:
			new_string = ' '.join(w_list)
			new_songlist.append([song_id,new_string,song_title])
			new_raw_words_list.append([count, [song_id, w_list]])

	return raw_word_count, new_songlist, new_raw_words_list, tot_count


# stop words
def stop_words(filtered, new_raw_words_list, language):

	stops = stopwords.words(language)

	db_words_list = []
	frequencies = []
	results = {}
	graph_list = []
	for words_list in new_raw_words_list: # [count, [song_id, raw_words] ]
		count = words_list[0]
		song_id = words_list[1][0]
		raw_words = words_list[1][1]
		no_stop_words = [w for w in raw_words if w.lower() not in stops]
		if filtered:
			words_count = Counter(no_stop_words)
		else:
			words_count = Counter(raw_words)

		if filtered:
			graph_list.append(no_stop_words)
		else:
			graph_list.append(raw_words)

		db_words_list.append([song_id, words_count])
		
		# save the results
		results = sorted(
			words_count.items(),
			key=operator.itemgetter(1),
			reverse=True
		)[:10]

		#----------------------------------------
		# frequencies = [ song_id, Word, Count ]
		#----------------------------------------
		frequencies.append([song_id, results, count])

	return graph_list, frequencies, db_words_list


# create results: frequencies, songs, graph_data, (counts)
def create_results(raw_word_count, db_words_list, frequencies, new_songlist, graph_list, word_to_find, tot_count):

	# counts per song
	counts = []
	for item in frequencies:
		counts.append(item[2])

	#----------------------------------------
	# songs = [ song_id, Markup(new_string), song_title ]
	#----------------------------------------
	# Markup song list
	songs = []
	for item in new_songlist:
		song_id = item[0]
		new_string = item[1]
		song_title = item[2]
		words = item[1].split(' ')
		w_list = []
		for word in words:
			if word.lower() == word_to_find.lower():
				word = r"<mark><strong>"+word+"</strong></mark>"
			w_list.append(word)
		new_string = ' '.join(w_list)
		songs.append([item[0],Markup(new_string),item[2]])

	#----------------------------------------
	# graph_data = {}
	#----------------------------------------
	values = []
	for item in graph_list:
		for word in item:
			values.append(word)
	values_count = Counter(values)
	graph_data = sorted(
		values_count.items(),
		key=operator.itemgetter(1),
		reverse=True
	)[:10]

	return frequencies, songs, graph_data, counts


# database storing
def store_db(raw_word_count, db_words_list, word_to_find, counts):

	# database
	for i in range(len(raw_word_count)):
		try:
			result = Words(
				word = word_to_find,
				matches = counts[i],
				result_all = raw_word_count[i],
				result_no_stop_words = db_words_list[i][1]
			)
			result.song_id = db_words_list[i][0]

			db.session.add(result)
			db.session.commit()
		except SQLAlchemyError:
			db.session.rollback()
			flash("Unable to add item to Words database.", "danger")
			break

	return
	
