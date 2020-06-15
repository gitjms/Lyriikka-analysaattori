from flask import render_template, redirect, flash, url_for, request, g, Markup
from flask_login import current_user

from application import app, db, login_manager, login_required
from application.songs.models import Song
from application.poems.models import Poem
from application.words.models import Words
from application.words.proc import proc_text, stop_words, create_results, store_search_word


@app.before_request
def before_request():
	g.user = current_user


#-----------------------------------------
#		SHOW: words_find()
#-----------------------------------------
@app.route("/words/find/", methods=["GET", "POST"])
@login_required
def words_find():
	filtered = False
	save = False
	material = request.form.get('fromchoice')

	if g.user.role == "GUEST" or g.user.role == "ADMIN":
		user_list = [1,2]
	else:
		user_list = [1,g.user.id]

	if request.method == "GET":
		return redirect(url_for("index"))

	if request.method == "POST":
		if request.form.get('filter') is None:
			if request.form.get('wordsearch') is not None:
				word_to_find = request.form.get('wordsearch').strip()
			if request.form.get('langchoice') is not None:
				language = request.form.get('langchoice')
			material = request.form.get('fromchoice')
		elif request.form.get('filter') is not None:
			data = request.form.get('filter').split(',')
			word_to_find = data[0].strip()
			language = data[1]
			material = data[3]
			if data[2] == "True":
				filtered = False
			elif data[2] == "False":
				filtered = True
		
		if request.form.get('save') is not None:
			data = request.form.get('save').split(',')
			word_to_find = data[0].strip()
			language = data[1]
			if data[2] == "True":
				filtered = True
			elif data[2] == "False":
				filtered = False
			material = data[3]
			save = True
	
	#-------------------------------------------------------
	# get data from database
	#
	#-------------------------------------------------------
	if material == 'Song':
		materials = Song.query.filter(Song.account_id.in_(user_list)).all()
		if not materials:
			return render_template("words/words.html", frequencies = None, materials=None)
		title_text = 'Top 10 Word Frequencies in Match Song(s)'
	elif material == 'Poem':
		materials = Poem.query.filter(Poem.account_id.in_(user_list)).all()
		if not materials:
			return render_template("words/words.html", frequencies = None, materials=None)
		title_text = 'Top 10 Word Frequencies in Match Poem(s)'

	# qry_list = [ song_id, lyrics, song_name, language ]
	if material == 'Song':
		qry_list = db.session().query(Song.id,Song.lyrics,Song.name,Song.language).filter(Song.account_id.in_(user_list)).filter(Song.language==language).all()
	elif material == 'Poem':
		qry_list = db.session().query(Poem.id,Poem.lyrics,Poem.name,Poem.language).filter(Poem.account_id.in_(user_list)).filter(Poem.language==language).all()
		
	# prepare data
	material_list = []
	for i in qry_list:
		material_list.append([i[0], replace_chars(i[1]), i[2]])

	#-------------------------------------------------------
	# process lyrics
	# 
	# -> proc.proc_text()
	#
	#-------------------------------------------------------
	# raw_word_count = [ Counter(raw_words) ] => word counts
	# new_material_list = [ song_id/poem_id, new_string, song_name/poem_name ] => songs/poems w/o punctuation
	# new_raw_words_list = [ count, [song_id/poem_id, raw_words] ] => word lists
	#-------------------------------------------------------
	raw_word_count, new_material_list, new_raw_words_list, tot_count = proc_text(material_list, word_to_find, graph="")
	
	#-------------------------------------------------------
	# stop words, get count data for html and graph
	# 
	# -> proc.stop_words()
	#
	#-------------------------------------------------------
	# graph_list = [ raw_words ] => with or without stopwords
	# results_list = [ song_id/poem_id, Word, Count ] => for frequency tables
	# words_list = [ song_id/poem_id, Counter() ] => for database storing
	#-------------------------------------------------------
	if tot_count > 0:
		graph_list, results_list, db_words_list = stop_words(filtered, new_raw_words_list, language, graph="")
	else:
		return render_template("words/words.html", frequencies = None, word=word_to_find)

	#-------------------------------------------------------
	# create results: res_material, graph_data, (counts)
	# 
	# -> proc.create_results()
	#
	#-------------------------------------------------------
	frequencies = None
	res_material = None
	if tot_count > 0:
		
		res_material, graph_data = create_results(new_material_list, graph_list, word_to_find)

	#-------------------------------------------------------
	# store to database
	# 
	# -> proc.store_search_word()
	#
	#-------------------------------------------------------
	errors = []
	is_already = Words.query.filter_by(result_all=word_to_find).first()
	
	if save == True and tot_count > 0 and Words.query.filter_by(word=word_to_find).first() is None:
		# counts per song
		counts = []
		for item in results_list:
				counts.append(item[2])

		errors = store_search_word(raw_word_count, db_words_list, word_to_find, counts)

	elif save == True and tot_count > 0 and Words.query.filter_by(word=word_to_find).first() is not None:
		errors.append("Results already in the database.")
		flash("Results not added to results database.", "warning")

	return render_template("words/words.html", frequencies=results_list, res_material=replace_accent(res_material), word=word_to_find, errors=errors, count=tot_count, material_count=len(new_material_list), graph_data=graph_data, language=language, filtered=filtered, material=material, title_text=title_text)


# own stopwords
def replace_chars(text):
	for ch in ['\\n','V1','V2','V3','V4','V5','V6','V7','V8','V9','V10','B1','B2','B3','B4','B5','B6','B7','B8','B9','B10','C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','P1','P2','P3','P4','P5','P6','P7','P8','P9','P10'," I "," II "," III "," IV "," V "," VI "," VII "," VIII "," IX "," X ",'\'n','\n','\'n\'n','\'r','\'r\'n',"'ll","'s","'d","'t"]:
		if ch == "œ" and ch in text:
			text = text.replace(ch,"oe")
		if ch in text:
			text = text.replace(ch,"")
	return text


# difficult accent for Source(s) lyrics html in Results page
def replace_accent(text):
	for item in text:
		if "\´" in item[1]:
			item[1] = item[1].replace("\´","\'")
		if "œ" in item[1]:
			item[1] = item[1].replace("œ","oe")
	return text
