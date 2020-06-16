from flask import redirect, url_for, render_template, request, flash, g
from flask_login import current_user

from application import app, db, login_manager, login_required
from application.poems.models import Poem
from application.auth.models import User
from application.poets.models import Poet
from application.poets.proc import prepare_data, proc_poets, store_results
from application.words.views import replace_accent

from collections import Counter

@app.before_request
def before_request():
	g.user = current_user


#-----------------------------------------
#		POETS: poets_list()
#-----------------------------------------
@app.route("/poets/list", methods=["GET", "POST"])
@login_required(roles=[1,2,3])
def poets_list():

	poets = Poet.get_poets("")
	if poets:
		return render_template("poets/list.html", poets=poets)
	else:
		return render_template("poets/list.html", poets=None)


#-----------------------------------------
#		POETS: poets_graph()
#-----------------------------------------
@app.route("/poets/graph", methods=["GET", "POST"])
@login_required(roles=[1,2,3])
def poets_graph():
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
	# get data: poets = [ name, lyrics, language, id ]
	# get poet
	#-------------------------------------------------------
	poets_en = Poet.get_poets('english')
	results_en = []
	for row in poets_en:
		results_en.append(get_results(poet_id=row['id'], filtered=filtered, type='graph', lang='english'))

	poets_fi = Poet.get_poets('finnish')
	results_fi = []
	for row in poets_fi:
		results_fi.append(get_results(poet_id=row['id'], filtered=filtered, type='graph', lang='finnish'))

	poets_fr = Poet.get_poets('french')
	results_fr = []
	for row in poets_fr:
		results_fr.append(get_results(poet_id=row['id'], filtered=filtered, type='graph', lang='french'))

	table_en, table_fi, table_fr, graph_en, graph_fi, graph_fr = prepare_data(results_en, results_fi, results_fr)


	return render_template("poets/graph.html", table_en=table_en, table_fi=table_fi, table_fr=table_fr, graph_en=graph_en, graph_fi=graph_fi, graph_fr=graph_fr, filtered=filtered)


#-----------------------------------------
#		POETS: poets_show()
#-----------------------------------------
@app.route("/poets/show/<poet_id>", methods=["GET", "POST"])
@login_required(roles=[1,2,3])
def poets_show(poet_id):
	graphs = False
	filtered = False
	save = False

	if request.method == "GET":
		return render_template("poets/show.html", poet = Poet.query.get(poet_id), graphs=graphs)

	if request.method == "POST":

		if request.form.get("Back") == "Back":
			return redirect(url_for("poets_list"))

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

		poet, results_list, db_words_list, graph_data, raw_word_count, new_poemlist, language = get_results(poet_id, filtered, type="", lang="")

		#-------------------------------------------------------
		# store to database
		#-------------------------------------------------------
		errors = []
		if save == True and poet.result_all is None:
			errors = store_results(poet, results_list, raw_word_count, db_words_list)
		elif save == True and poet.result_all is not None:
			errors.append("Results already in the database.")
			flash("Results not added to Poet database.", "warning")

		return render_template("poets/show.html", poet=poet, frequencies=results_list, poems=replace_accent(new_poemlist), errors=errors, graph_data=graph_data, language=language, filtered=filtered, graphs=graphs)

	return render_template("poets/show.html", poet = Poet.query.get(poet_id), graphs=graphs, type=type, lang="")


#-----------------------------------------
#	get_results()
#-----------------------------------------
def get_results(poet_id, filtered, type, lang):

	# poet_poems = [ poem_id, lyrics, language ]
	poet_poems = Poet.get_poetpoems(poet_id)
	poet = Poet.query.get(poet_id)

	if type == 'graph':
		graph_data, table_data, language = proc_poets(poet_poems, filtered, lang)
		return poet.name, graph_data, table_data, language
	else:
		results_list, db_words_list, graph_data, raw_word_count, new_poemlist, language = proc_poets(poet_poems, filtered, lang)
		return poet, results_list, db_words_list, graph_data, raw_word_count, new_poemlist, language

