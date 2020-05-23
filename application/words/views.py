from flask import render_template, request, g
# from flask_wtf import FlaskForm
from flask_login import login_required, current_user


from application import app, db
from application.songs.models import Song
from application.words.forms import WordForm
# STOPWORDS FROM CATALOGUES:
# from nltk.corpus import stopwords
# OWN STOPWORDS:
# from application.stopwords.stopwords import stops
from application.textproc.proc import proc_text, stop_words, store_db

# Lomakkeen näyttämisen ja lähetyksen vastaanottava toiminnallisuus.

@app.before_request
def before_request():
	g.user = current_user


#-----------------------------------------
#		SHOW: words_find()
#-----------------------------------------
@app.route("/words/show/", methods=["GET", "POST"])
@login_required
def words_find():
	errors = []

	user_list = [g.user.id,1]
	form = WordForm(request.form)
	word_to_find = request.form['wordsearch']
	language = request.form['langchoice']

	# get data from database
	qry_list = db.session().query(Song.id,Song.lyrics,Song.title).filter(Song.account_id.in_((user_list))).all()
	song_list = []
	for i in qry_list:
		raw_to_string = ' '.join([str(elem) for elem in i])
		song_list.append([i[0], replace_chars(raw_to_string),i[2]])

	# process lyrics
	raw_word_count, new_songlist, new_raw_words_list, tot_count = proc_text(song_list, word_to_find)
	
	# stop words, get count data for html and graph
	graph_list, results_list, no_stop_words_list = stop_words(new_raw_words_list, language)

	# store to database
	page_results = None
	page_songs = None
	if tot_count > 0:
		page_results, page_songs, result_values = store_db(raw_word_count, no_stop_words_list, results_list, new_songlist, graph_list, word_to_find, tot_count)

	return render_template("words/words.html", frequencies = page_results, songs=page_songs, word=word_to_find, errors=errors, count = tot_count, song_count=len(new_songlist), graph_data=result_values)


def replace_chars(text):
	for ch in ['\\n','BRIDGE','POST-CHORUS','CHORUS','VERSE','V1','V2','V3','V4','V5','V6','V7','V8','V9','V10','B1','B2','B3','B4','B5','B6','B7','B8','B9','B10','C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','\'n','\n','\'n\'n','\'r','\'r\'n']:
		if ch in text:
			text = text.replace(ch,"")
	return text
