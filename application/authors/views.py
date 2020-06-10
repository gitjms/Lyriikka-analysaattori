from flask import redirect, url_for, render_template, request, flash, g
from flask_login import current_user

from application import app, db, login_manager, login_required
from application.songs.models import Song
from application.auth.models import User
from application.authors.models import Author
from application.authors.proc import prepare_data, proc_authors, store_results
from application.words.views import replace_accent

from collections import Counter

@app.before_request
def before_request():
	g.user = current_user


#-----------------------------------------
#		AUTHORS: authors_list()
#-----------------------------------------
@app.route("/authors/list", methods=["GET", "POST"])
@login_required
def authors_list():

	authors = Author.get_authors("")
	if authors:
		return render_template("authors/list.html", authors=authors)
	else:
		return render_template("authors/list.html", authors=None)


#-----------------------------------------
#		AUTHORS: authors_graph()
#-----------------------------------------
@app.route("/authors/graph", methods=["GET", "POST"])
@login_required
def authors_graph():
	filtered = False
	save = False

	if request.method == "POST":
			
		if request.form.get('filter') is not None:
			data = request.form.get('filter').split(',')
			if data[0] == "True":
				filtered = False
			elif data[0] == "False":
				filtered = True
		
		if request.form.get('save') is not None:
			data = request.form.get('save').split(',')
			if data[0] == "True":
				filtered = True
			elif data[0] == "False":
				filtered = False
			save = True

	#-------------------------------------------------------
	# get data: authors = [ name, lyrics, language, id ]
	# get author
	#-------------------------------------------------------
	authors_en = Author.get_authors('english')
	results_en = []
	for row in authors_en:
		results_en.append(get_results(author_id=row['id'], filtered=filtered, type='graph', lang='english'))

	authors_fi = Author.get_authors('finnish')
	results_fi = []
	for row in authors_fi:
		results_fi.append(get_results(author_id=row['id'], filtered=filtered, type='graph', lang='finnish'))

	authors_fr = Author.get_authors('french')
	results_fr = []
	for row in authors_fr:
		results_fr.append(get_results(author_id=row['id'], filtered=filtered, type='graph', lang='french'))

	table_en, table_fi, table_fr, graph_en, graph_fi, graph_fr = prepare_data(results_en, results_fi, results_fr)


	return render_template("authors/graph.html", table_en=table_en, table_fi=table_fi, table_fr=table_fr, graph_en=graph_en, graph_fi=graph_fi, graph_fr=graph_fr, filtered=filtered)


#-----------------------------------------
#		AUTHORS: authors_show()
#-----------------------------------------
@app.route("/authors/show/<author_id>", methods=["GET", "POST"])
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

		author, results_list, db_words_list, graph_data, raw_word_count, new_songlist, language = get_results(author_id, filtered, type="", lang="")

		#-------------------------------------------------------
		# store to database
		#-------------------------------------------------------
		errors = []
		if save == True and author.result_all is None:
			errors = store_results(author, results_list, raw_word_count, db_words_list)
		elif save == True and author.result_all is not None:
			errors.append("Results already in the database.")
			flash("Results not added to Author database.", "warning")

		return render_template("authors/show.html", author=author, frequencies=results_list, songs=replace_accent(new_songlist), errors=errors, graph_data=graph_data, language=language, filtered=filtered, graphs=graphs)

	return render_template("authors/show.html", author = Author.query.get(author_id), graphs=graphs, type=type, lang="")


#-----------------------------------------
#	get_results()
#-----------------------------------------
def get_results(author_id, filtered, type, lang):

	# author_songs = [ song_id, lyrics, language ]
	author_songs = Author.get_authorsongs(author_id)
	author = Author.query.get(author_id)

	if type == 'graph':
		graph_data, table_data, language = proc_authors(author_songs, filtered, lang)
		return author.name, graph_data, table_data, language
	else:
		results_list, db_words_list, graph_data, raw_word_count, new_songlist, language = proc_authors(author_songs, filtered, lang)
		return author, results_list, db_words_list, graph_data, raw_word_count, new_songlist, language

