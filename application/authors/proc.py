from flask import flash

from application.words.views import replace_chars, replace_accent
from application.words.proc import proc_text, stop_words, create_results, store_author_words


def proc_authors(author_songs, filtered):

	#-------------------------------------------------------
	# prepare data
	#-------------------------------------------------------
	song_list = []
	for i in author_songs:
		song_list.append([i['id'], replace_chars(i['lyrics']), i['title'], i['language']])
		language = i['language']

	#-------------------------------------------------------
	# process data
	#-------------------------------------------------------
	# raw_word_count = [ Counter(raw_words) ] => word counts
	# new_songlist = [ song_id, new_string, song_name ] => songs w/o punctuation
	# new_raw_words_list = [ count=0, [song_id, raw_words] ] => word lists
	#-------------------------------------------------------
	raw_word_count, new_songlist, new_raw_words_list = proc_text(song_list, None)

	#-------------------------------------------------------
	# stop words
	#-------------------------------------------------------
	# graph_list = [ raw_words ] => word lists for graph
	# results_list = [ song_id, Word=None, Count=0 ] => top 10 word frequencies
	# db_words_list = [ song_id, Counter() ] => for database storing
	#-------------------------------------------------------
	graph_list, results_list, db_words_list = stop_words(filtered, new_raw_words_list, language, limit=5)

	#-------------------------------------------------------
	# get results
	#-------------------------------------------------------
	# graph_data = {}
	#-------------------------------------------------------
	frequencies = None
	graph_data = create_results(raw_word_count, db_words_list, None, graph_list, None, 0)

	return results_list, db_words_list, graph_data, raw_word_count, new_songlist, language


def store_results(author, results_list, raw_word_count, db_words_list):

	#-------------------------------------------------------
	# store to database
	#-------------------------------------------------------
	# counts per song
	counts = []
	for item in results_list:
		counts.append(item[2])

	errors = store_author_words(author, raw_word_count, db_words_list, counts)

	return errors
