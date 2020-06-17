from flask import render_template, redirect, flash, url_for, request, g, Markup
from flask_login import current_user

from sqlalchemy import or_

from application import app, db, login_manager, login_required
from application.songs.models import Song
from application.poems.models import Poem
from application.words.models import Words
from application.words.proc import proc_text, stop_words, create_results, store_search_word


@app.before_request
def before_request():
	g.user = current_user


@login_required(roles=[1,2,3])
def check_data(payload, which):
	if payload is not None:
		data = payload.split(',')
		word_to_find = data[0].strip()
		language = data[1]
		if data[2] == "True" and which == 'filter':
			filtered = False
		elif data[2] == "True" and which == 'save':
			filtered = True
		elif data[2] == "False" and which == 'filter':
			filtered = True
		elif data[2] == "False" and which == 'save':
			filtered = False
		material = data[3]

	return word_to_find, language, filtered, material


#-----------------------------------------
#		SHOW: words_find()
#-----------------------------------------
@app.route("/words/find/", methods=["GET", "POST"])
@login_required(roles=[1,2,3])
def words_find():
	filtered = False
	save = False
	word = None
	material = None
	language = None
	frequencies = None
	res_material = None

	if request.method == "GET":
		return redirect(url_for("index"))

	if request.form.get('filter') is None:
		if request.form.get('wordsearch') is not None:
			word_to_find = request.form.get('wordsearch').strip()
		if request.form.get('langchoice') is not None:
			language = request.form.get('langchoice')
		material = request.form.get('fromchoice')
	else:
		word_to_find, language, filtered, material = check_data(request.form.get('filter'), 'filter')

	if request.form.get('save') is not None:
		word_to_find, language, filtered, material = check_data(request.form.get('save'), 'save')
		save = True
	
	#-------------------------------------------------------
	# get data from database
	#
	#-------------------------------------------------------
	if material == 'Song':
		materials = db.session().query(Song.id,Song.lyrics,Song.name,Song.language).filter(or_(Song.account_id==g.user.id,Song.account_role==1)).filter(Song.language==language).all()
		if not materials:
			return render_template("words/words.html", frequencies = frequencies)
		title_text = 'Top 10 Word Frequencies in Match Song(s)'
	elif material == 'Poem':
		materials = db.session().query(Poem.id,Poem.lyrics,Poem.name,Poem.language).filter(or_(Poem.account_id==g.user.id,Poem.account_role==1)).filter(Poem.language==language).all()
		if not materials:
			return render_template("words/words.html", frequencies = frequencies)
		title_text = 'Top 10 Word Frequencies in Match Poem(s)'

	if not language:
		return render_template("words/words.html", language=language)

	# prepare data
	material_list = []
	for i in materials:
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
	# frequencies = [ song_id/poem_id, Word, Count ] => for frequency tables
	# words_list = [ song_id/poem_id, Counter() ] => for database storing
	#-------------------------------------------------------
	if tot_count > 0:
		graph_list, frequencies, db_words_list = stop_words(filtered, new_raw_words_list, language, graph="")
	else:
		return render_template("words/words.html", frequencies = None, word=word_to_find)

	#-------------------------------------------------------
	# create results: res_material, graph_data, (counts)
	# 
	# -> proc.create_results()
	#
	#-------------------------------------------------------
	if tot_count > 0:
		
		res_material, graph_data = create_results(new_material_list, graph_list, word_to_find)

	#-------------------------------------------------------
	# store to database
	# 
	# -> proc.store_search_word()
	#
	#-------------------------------------------------------
	errors = []
	
	if save == True and tot_count > 0 and Words.query.filter_by(word=word_to_find).first() is None:
		# counts per song
		counts = []
		for item in frequencies:
				counts.append(item[2])

		errors = store_search_word(raw_word_count, db_words_list, word_to_find, counts)

	elif save == True and tot_count > 0 and Words.query.filter_by(word=word_to_find).first() is not None:
		errors.append("Results already in the database.")
		flash("Results not added to results database.", "warning")

	return render_template("words/words.html", frequencies=frequencies, res_material=replace_accent(res_material), word=word_to_find, errors=errors, count=tot_count, material_count=len(new_material_list), graph_data=graph_data, language=language, filtered=filtered, material=material, title_text=title_text)


# own stopwords
@login_required(roles=[1,2,3])
def replace_chars(text):
	for ch in ['\\n','V1','V2','V3','V4','V5','V6','V7','V8','V9','V10','B1','B2','B3','B4','B5','B6','B7','B8','B9','B10','C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','P1','P2','P3','P4','P5','P6','P7','P8','P9','P10'," I "," II "," III "," IV "," V "," VI "," VII "," VIII "," IX "," X ",'\'n','\n','\'n\'n','\'r','\'r\'n',"'ll","'s","'d","'t"]:
		if ch == "œ" and ch in text:
			text = text.replace(ch,"oe")
		if ch in text:
			text = text.replace(ch,"")
	return text


# difficult accent for Source(s) lyrics html in Results page
@login_required(roles=[1,2,3])
def replace_accent(text):
	for item in text:
		if "\´" in item[1]:
			item[1] = item[1].replace("\´","\'")
		if "œ" in item[1]:
			item[1] = item[1].replace("œ","oe")
	return text
