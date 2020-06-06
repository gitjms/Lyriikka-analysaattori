from flask import redirect, url_for, render_template, request, flash, g
from flask_login import current_user

from sqlalchemy.sql import text

from application import app, db, login_manager, login_required
from application.songs.models import Song
from application.auth.models import User
from application.authors.models import Author, author_song
from application.words.views import replace_chars, replace_accent
from application.words.proc import proc_text, stop_words, create_results

@app.before_request
def before_request():
	g.user = current_user


#-----------------------------------------
#		AUTHORS: authors_list()
#-----------------------------------------
@app.route("/authors/list", methods=["GET", "POST"])
@login_required
def authors_list():

	if request.form.get("Back") == "Back":
		return redirect(url_for("songs_home"))

	authors = Author.get_authors()
	if authors:
		return render_template("authors/list.html", authors=authors)
	else:
		return render_template("authors/list.html", authors=None)


#-----------------------------------------
#		AUTHORS: authors_show()
#-----------------------------------------
@app.route("/authors/show/<author_id>/", methods=["GET", "POST"])
@login_required
def authors_show(author_id):
	filtered = False

	if request.method == "POST":

		if request.form.get("Back") == "Back":
			return redirect(url_for("authors_list"))

		if request.form.get('filter') == "True":
			filtered = False
		elif request.form.get('filter') == "False":
			filtered = True


	if request.method == "GET":

		# get data: author_songs = [ song_id, lyrics, language ]
		author_songs = Author.get_authorsongs(author_id)

		# prepare data
		song_list = []
		for i in author_songs:
			song_list.append([i['id'], replace_chars(i['lyrics']), i['language']])
			language = i['language']

		# process data
		# raw_word_count = [ Counter(raw_words) ] => word counts
		# new_songlist = [ song_id, new_string, song_name ] => songs w/o punctuation
		# new_raw_words_list = [ count=0, [song_id, raw_words] ] => word lists
		raw_word_count, new_songlist, new_raw_words_list = proc_text(song_list, None)

		# stop words
		# graph_list = [ raw_words ] => word lists for graph
		# results_list = [ song_id, Word=None, Count=0 ] => top 10 word frequencies
		# db_words_list = [ song_id, Counter() ] => for database storing
		graph_list, results_list, db_words_list = stop_words(filtered, new_raw_words_list, language)

		# counts per song (for database storing)
		# counts = []
		# for item in results_list:
			# counts.append(item[2])

		# get results
		# graph_data = {}
		frequencies = None
		songs = None
		graph_data = create_results(raw_word_count, db_words_list, None, graph_list, None, 0)


		print('\n\n\n',results_list,'\n\n')
		print('\n\n\n',songs,'\n\n\n')
		print('\n\n\n',graph_data,'\n\n\n')
		print('\n\n\n',counts,'\n\n\n')


		return render_template("authors/show.html", author = Author.query.get(author_id), frequencies = results_list, songs=replace_accent(songs), errors=errors, song_count=len(new_songlist), graph_data=graph_data, language=language, filtered=filtered)



