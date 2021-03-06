from flask import flash, g, Markup

import os
from unidecode import unidecode
import operator
import re
import nltk
nltk.download('punkt')
from application.words import ownstops
from collections import Counter

from application import db, login_manager, login_required
from application.words.models import Word
from application.songs.models import Song

from sqlalchemy.exc import IntegrityError, SQLAlchemyError


# raw words count
@login_required(roles=[1,2,3])
def proc_text(song_list, word_to_find, graph):

	text_list = [] # [ song_id, lyrics, song_name ]
	nltk.data.path.append(os.getcwd()+'/application/nltk_data/')

	for song in song_list:
		tokens = nltk.word_tokenize(song[1])
		text_list.append([song[0], nltk.Text(tokens), song[2]])

	# remove punctuation, count raw words
	raw_word_count = [] # [ Counter(raw_words) ]
	raw_words_list = [] # [ song_id, raw_words ]
	for txt in text_list: # [ song_id, lyrics, song_name ]
		count = 0
		raw_words = []
		song_id = txt[0]
		lyrics = txt[1]
		song_name = txt[2]
		nonPunct = re.compile('.*[A-Za-z].*')
		for i in lyrics:
			if nonPunct.match(i):
				raw_words.append(i.lower())
			if word_to_find is not None and unidecode(i.lower()) == unidecode(word_to_find.lower()):
				count += 1
		if (word_to_find is not None and count > 0) or (word_to_find is None and count == 0):
			raw_words_list.append([song_id, raw_words, song_name])
			raw_word_count.append(Counter(raw_words))

	# count matches and store source text without newlines
	new_songlist = [] # [ song_id, new_string, song_name ]
	new_raw_words_list = []
	tot_count = 0
	for item in raw_words_list: # [ song_id, raw_words, song_name ]
		w_list = []
		count = 0
		song_id = item[0]
		raw_words = item[1]
		song_name = item[2]
		for w in raw_words:
			if word_to_find is not None and unidecode(w.lower()) == unidecode(word_to_find.lower()):
				count += 1
				tot_count += 1
			w_list.append(w)
		if (word_to_find is not None and count > 0) or (word_to_find is None and count == 0):
			new_string = ' '.join(w_list)
			new_songlist.append([song_id,new_string,song_name])
			new_raw_words_list.append([count, [song_id, w_list]])

	if word_to_find is not None:
		return raw_word_count, new_songlist, new_raw_words_list, tot_count
	else:
		if graph == "":
			return raw_word_count, new_songlist, new_raw_words_list
		else:
			return new_raw_words_list


# stop words
@login_required(roles=[1,2,3])
def stop_words(filtered, new_raw_words_list, language, graph):

	# stops = stopwords.words(language)
	if language == 'english':
		stops = ownstops.stops_en
	elif language == 'french':
		stops = ownstops.stops_fr
	elif language == 'finnish':
		stops = ownstops.stops_fi

	if graph == "":
		db_words_list = []
		results_list = []
		results = {}
	graph_list = []
	for words_list in new_raw_words_list: # [ count, [song_id, raw_words] ]
		count = words_list[0]
		song_id = words_list[1][0]
		raw_words = words_list[1][1]
		raw_words_graph = [w.lower() for w in raw_words if w.lower()]
		no_stop_words = [w.lower() for w in raw_words if w.lower() not in stops]
		if filtered:
			graph_list.append(no_stop_words)
		else:
			graph_list.append(raw_words_graph)

		if graph == "":
			words_count = Counter(replace_for_table(no_stop_words))
			db_words_list.append([song_id, words_count])
		
			# save the results for frequency tables
			results = sorted(
				words_count.items(),
				key=operator.itemgetter(1),
				reverse=True
			)[:10]

			#----------------------------------------
			# results_list = [ song_id, Word, Count ]
			#----------------------------------------
			results_list.append([song_id, results, count])

	if graph == "":
		return graph_list, results_list, db_words_list
	else:
		return graph_list


#-----------------------------------------
# create results: (songs,) graph_data
#-----------------------------------------
@login_required(roles=[1,2,3])
def create_results(new_songlist, graph_list, word_to_find):

	if word_to_find is not None:
		#----------------------------------------
		# songs = [ song_id, Markup(new_string), song_name ]
		#----------------------------------------
		# Markup song list
		songs = []
		for item in new_songlist:
			song_id = item[0]
			new_string = item[1]
			song_name = item[2]
			words = item[1].split(' ')
			w_list = []
			for word in words:
				if unidecode(word.lower()) == unidecode(word_to_find.lower()):
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

	if word_to_find is not None:
		return songs, graph_data
	else:
		return graph_data


#-----------------------------------------
# create results: graph_data, (table_data)
#-----------------------------------------
@login_required(roles=[1,2,3])
def create_results_graph(graph_list, graph, limit):

	#----------------------------------------
	# graph_data = {}
	#----------------------------------------
	values_graph = []
	for item in graph_list:
		for word in item:
			values_graph.append(word)
	values_graph_count = Counter(replace_graph(values_graph))
	graph_data = sorted(
		values_graph_count.items(),
		key=operator.itemgetter(1),
		reverse=True
	)[:10]

	if graph == "graph":
		#----------------------------------------
		# table_data = {}
		#----------------------------------------
		values_table = []
		for item in graph_list:
			for word in item:
				values_table.append(word)
		values_table_count = Counter(replace_for_table(values_table))
		table_data = sorted(
			values_table_count.items(),
			key=operator.itemgetter(1),
			reverse=True
		)[:limit]
		
	if graph == "graph":
		return graph_data, table_data
	else:
		return graph_data


#-----------------------------------------
# database storing for search word results
#-----------------------------------------
@login_required(roles=[1,3])
def store_search_word(raw_word_count, db_words_list, word_to_find, counts):
	errors = []

	# database
	for i in range(len(raw_word_count)):
		try:
			result = Word(
				word = word_to_find.lower(),
				matches = counts[i],
				result_all = raw_word_count[i],
				result_no_stop_words = db_words_list[i][1]
			)
			id = Song.query.filter_by(id=db_words_list[i][0]).first().id
			result.songs.extend(Song.query.filter_by(id=id))

			db.session.add(result)
			db.session.commit()
		except SQLAlchemyError:
			db.session.rollback()
			errors.append("Unable to add item to database.")
			flash("Unable to add item to Words database.", "danger")
			break

	return errors


#-----------------------------------------
# database storing for author words results
#-----------------------------------------
@login_required(roles=[1,3])
def store_author_words(author, raw_word_count, db_words_list, counts, auteur):
	errors = []

	# database
	for i in range(len(raw_word_count)):
		try:
			author.result_all = raw_word_count[i]
			db.session.commit()
			author.result_no_stop_words = db_words_list[i][1]
			db.session.commit()
		except SQLAlchemyError:
			db.session.rollback()
			errors.append("Unable to add item to " + author + " database.")
			flash("Unable to add item to " + author + " database.", "danger")
			break

	return errors


# difficult accent for word frequency tables html in authors/graph page
@login_required(roles=[1,2,3])
def replace_for_table(list):
	for n, item in enumerate(list):
		if "\´" in item:
			list[n] = item.replace("\´","\'")
		if "œ" in item:
			list[n] = item.replace("œ","oe")
	return list


# difficult accent for Source(s) lyrics html in Results page
@login_required(roles=[1,2,3])
def replace_graph(list):
	for n, item in enumerate(list):
		if "\'" in item:
			list[n] = item.replace("\'","\´")
		if "œ" in item:
			list[n] = item.replace("œ","oe")
	return list
