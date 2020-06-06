from flask import redirect, url_for, render_template, request, flash, g
from flask_login import current_user

from sqlalchemy.sql import text

from application import app, db, login_manager, login_required
from application.songs.models import Song
from application.auth.models import User
from application.authors.models import Author, author_song
from application.words.views import replace_chars, replace_accent
from application.words.proc import proc_text, stop_words, create_results, store_author_words

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
	graphs = False
	filtered = False
	save = False

	if request.method == "GET":
		return render_template("authors/show.html", author = Author.query.get(author_id), graphs=graphs)

	if request.method == "POST":

		if request.form.get("Back") == "Back":
			return redirect(url_for("authors_list"))

		if request.form.get("graph") == "graph":
			graphs = True
			
		if request.form.get('filter') is not None:
			data = request.form.get('filter').split(',')
			graphs = data[1]
			if data[0] == "True":
				filtered = False
			elif data[0] == "False":
				filtered = True
		
		if request.form.get('save') is not None:
			data = request.form.get('save').split(',')
			graphs = data[1]
			if data[0] == "True":
				filtered = True
			elif data[0] == "False":
				filtered = False
			save = True

		#-------------------------------------------------------
		# get data: author_songs = [ song_id, lyrics, language ]
		# get author
		#-------------------------------------------------------
		author_songs = Author.get_authorsongs(author_id)

		author = Author.query.get(author_id)

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
		graph_list, results_list, db_words_list = stop_words(filtered, new_raw_words_list, language)

		#-------------------------------------------------------
		# get results
		#-------------------------------------------------------
		# graph_data = {}
		#-------------------------------------------------------
		frequencies = None
		graph_data = create_results(raw_word_count, db_words_list, None, graph_list, None, 0)

		#-------------------------------------------------------
		# store to database
		#-------------------------------------------------------
		errors = []
		if save == True and author.result_all is None:
			# counts per song
			counts = []
			for item in results_list:
					counts.append(item[2])

			errors = store_author_words(author, raw_word_count, db_words_list, counts)

		elif save == True and author.result_all is not None:
			errors.append("Results already in the database.")
			flash("Results not added to Author database.", "warning")

		return render_template("authors/show.html", author=author, frequencies=results_list, songs=replace_accent(new_songlist), errors=errors, graph_data=graph_data, language=language, filtered=filtered, graphs=graphs)
