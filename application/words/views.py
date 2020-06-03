from flask import render_template, redirect, flash, url_for, request, g, Markup
from flask_login import current_user

from application import app, db, login_manager, login_required
from application.songs.models import Song
from application.words.models import Words
from application.words.proc import proc_text, stop_words, create_results, store_db

# Lomakkeen näyttämisen ja lähetyksen vastaanottava toiminnallisuus.

@app.before_request
def before_request():
	g.user = current_user


#-----------------------------------------
#		SHOW: words_find()
#-----------------------------------------
@app.route("/words/find/", methods=["GET", "POST"])
@login_required
def words_find():
	errors = []
	filtered = False
	save = False

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
		elif request.form.get('filter') is not None:
			data = request.form.get('filter').split(',')
			word_to_find = data[0].strip()
			language = data[1]
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
			save = True
	
	#-------------------------------------------------------
	# get data from database
	#
	#-------------------------------------------------------
	qry_list = db.session().query(Song.id,Song.lyrics,Song.name,Song.language).filter(Song.account_id.in_(user_list)).filter(Song.language==language).all()

	song_list = []
	for i in qry_list:
		song_list.append([i[0], replace_chars(i[1]), i[2]])

	#-------------------------------------------------------
	# process lyrics
	# 
	# -> proc.proc_text()
	#
	#-------------------------------------------------------
	raw_word_count, new_songlist, new_raw_words_list, tot_count = proc_text(song_list, word_to_find)
	
	#-------------------------------------------------------
	# stop words, get count data for html and graph
	# 
	# -> proc.stop_words()
	#
	#-------------------------------------------------------
	if tot_count > 0:
		graph_list, results_list, words_list = stop_words(filtered, new_raw_words_list, language)
	else:
		return render_template("words/words.html", frequencies = None, word=word_to_find, errors=errors)

	#-------------------------------------------------------
	# create results: frequencies, songs, graph_data, (counts)
	# 
	# -> proc.create_results()
	#
	#-------------------------------------------------------
	frequencies = None
	songs = None
	if tot_count > 0:
		frequencies, songs, graph_data, counts = create_results(raw_word_count, words_list, results_list, new_songlist, graph_list, word_to_find, tot_count)

	#-------------------------------------------------------
	# store to database
	# 
	# -> proc.store_db()
	#
	#-------------------------------------------------------
	if save == True and tot_count > 0:
		store_db(raw_word_count, words_list, word_to_find, counts)

	return render_template("words/words.html", frequencies = frequencies, songs=replace_accent(songs), word=word_to_find, errors=errors, count = tot_count, song_count=len(new_songlist), graph_data=graph_data, language=language, filtered=filtered, save=save)


# own stopwords
def replace_chars(text):
	for ch in ['\\n','BRIDGE','POST-CHORUS','CHORUS','VERSE','V1','V2','V3','V4','V5','V6','V7','V8','V9','V10','B1','B2','B3','B4','B5','B6','B7','B8','B9','B10','C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','P1','P2','P3','P4','P5','P6','P7','P8','P9','P10','\'n','\n','\'n\'n','\'r','\'r\'n',"'ll","'s","\'"]:
		if ch == "\'" and ch in text:
			text = text.replace(ch,"\´")
		if ch in text:
			text = text.replace(ch,"")
	return text


# difficult accent for Source(s) lyrics html in Results page
def replace_accent(text):
	for item in text:
		if "\´" in item[1]:
			item[1] = item[1].replace("\´","\'")
	return text
