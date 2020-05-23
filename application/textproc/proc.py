from flask import flash, g, Markup

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
	nltk.data.path.append('./nltk_data/')
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

	return raw_word_count, new_songlist, new_raw_words_list, tot_count


# stop words
def stop_words(new_raw_words_list, lang):

	if lang == 'fi':
		stops = stopwords.words('finnish')
	elif lang == 'fr':
		stops = stopwords.words('french')
	else: # lang == 'en'
		stops = stopwords.words('english')

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

	return graph_list, results_list, no_stop_words_list


# database storing
def store_db(raw_word_count, no_stop_words_list, results_list, new_songlist, graph_list, word_to_find, tot_count):

	result_set = []
	result_set.append([raw_word_count, no_stop_words_list])
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

	# database
	for i in range(len(raw_word_count)):
		try:
			result = Words(
				word = word_to_find,
				matches = tot_count,
				result_all = raw_word_count[i],
				result_no_stop_words = no_stop_words_list[i][1]
			)
			result.word_song = no_stop_words_list[i][0]

			db.session.add(result)
			db.session.commit()
		except SQLAlchemyError:
			db.session.rollback()
			flash("Unable to add item to Words database.", "danger")
			errors.append("Unable to add item to Words database.")
			break

	return page_results, page_songs, result_values
	
