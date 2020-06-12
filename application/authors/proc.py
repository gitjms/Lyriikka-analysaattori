from flask import flash

from application.words.views import replace_chars
from application.words.proc import proc_text, stop_words, create_results, create_results_graph, store_author_words

from collections import Counter
import operator


#-------------------------------------------------------
# prepare data for authors_graph() html page
#-------------------------------------------------------
def prepare_data(results_en, results_fi, results_fr):

	author_names_en = [w[0] for w in results_en]
	author_names_fi = [w[0] for w in results_fi]
	author_names_fr = [w[0] for w in results_fr]
	graph_data_en = [dict(w[1]) for w in results_en]
	graph_data_fi = [dict(w[1]) for w in results_fi]
	graph_data_fr = [dict(w[1]) for w in results_fr]
	table_data_en = [w[2] for w in results_en]
	table_data_fi = [w[2] for w in results_fi]
	table_data_fr = [w[2] for w in results_fr]

	#---------------------------------------------------
	# combine graph dictonaries
	#---------------------------------------------------
	graph_dict_en = Counter({})
	for i in graph_data_en:
		count = Counter(i)
		graph_dict_en = graph_dict_en + count
	graph_dict_en = Counter(graph_dict_en)

	graph_en = sorted(
		Counter(graph_dict_en).items(),
		key=operator.itemgetter(1),
		reverse=True
	)[:10]

	graph_dict_fi = Counter({})
	for i in graph_data_fi:
		count = Counter(i)
		graph_dict_fi = graph_dict_fi + count
	graph_dict_fi = Counter(graph_dict_fi)

	graph_fi = sorted(
		Counter(graph_dict_fi).items(),
		key=operator.itemgetter(1),
		reverse=True
	)[:10]

	graph_dict_fr = Counter({})
	for i in graph_data_fr:
		count = Counter(i)
		graph_dict_fr = graph_dict_fr + count
	graph_dict_fr = Counter(graph_dict_fr)

	graph_fr = sorted(
		Counter(graph_dict_fr).items(),
		key=operator.itemgetter(1),
		reverse=True
	)[:10]

	#---------------------------------------------------
	# create table lists
	#---------------------------------------------------
	table_en = []
	for i in range(len(author_names_en)):
		table_en.append([author_names_en[i],[w for w in table_data_en[i]]])

	table_fi = []
	for i in range(len(author_names_fi)):
		table_fi.append([author_names_fi[i],[w for w in table_data_fi[i]]])

	table_fr = []
	for i in range(len(author_names_fr)):
		table_fr.append([author_names_fr[i],[w for w in table_data_fr[i]]])


	return table_en, table_fi, table_fr, graph_en, graph_fi, graph_fr
	

#-------------------------------------------------------
# process data
# for authors_show() return:
#	results_list, db_words_list, graph_data,
#	raw_word_count, new_songlist, language
# for authors_graph() return:
#	graph_data, table_data, language
#-------------------------------------------------------
def proc_authors(author_songs, filtered, lang):

	#---------------------------------------------------
	# prepare data
	#---------------------------------------------------
	song_list = []
	if lang == "":
		for i in author_songs:
			song_list.append([i['id'], replace_chars(i['lyrics']), i['title'], i['language']])
			language = i['language']
	else:
		for i in author_songs:
			if i['language'] == lang:
				song_list.append([i['id'], replace_chars(i['lyrics']), i['title'], i['language']])
				language = i['language']

	#---------------------------------------------------
	# process data
	#---------------------------------------------------
	# raw_word_count = [ Counter(raw_words) ] => word counts
	# new_songlist = [ song_id, new_string, song_name ] => songs w/o punctuation
	# new_raw_words_list = [ count=0, [song_id, raw_words] ] => word lists
	#---------------------------------------------------
	if lang == "":
		raw_word_count, new_songlist, new_raw_words_list = proc_text(song_list, None, graph="")
	else:
		new_raw_words_list = proc_text(song_list, None, graph="graph")

	#---------------------------------------------------
	# stop words
	#---------------------------------------------------
	# graph_list = [ raw_words ] => word lists for graph
	# results_list = [ song_id, Word=None, Count=0 ] => top 5 or 10 word frequencies
	# db_words_list = [ song_id, Counter() ] => for database storing
	#---------------------------------------------------
	if lang == "":
		graph_list, results_list, db_words_list = stop_words(filtered, new_raw_words_list, language, graph="")
	else:
		graph_list = stop_words(filtered, new_raw_words_list, language, graph="graph")

	#---------------------------------------------------
	# get results
	#---------------------------------------------------
	frequencies = None

	if lang == "":
		graph_data = create_results_graph(graph_list, graph="", limit=5)
		return results_list, db_words_list, graph_data, raw_word_count, new_songlist, language
	else:
		graph_data, table_data = create_results_graph(graph_list, graph="graph", limit=10)
		return graph_data, table_data, language


#-------------------------------------------------------
# store to database
#-------------------------------------------------------
def store_results(author, results_list, raw_word_count, db_words_list):

	# counts per song
	counts = []
	for item in results_list:
		counts.append(item[2])

	errors = store_author_words(author, raw_word_count, db_words_list, counts, auteur='Author')

	return errors

