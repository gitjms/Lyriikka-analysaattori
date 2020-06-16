from flask import url_for, redirect, render_template, request, flash, g, Response
from flask_login import current_user

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.sql import func, text

from application import app, db, login_manager, login_required
from application.auth.models import User
from application.songs.models import Song
from application.authors.models import Author
from application.authors.models import author_song
from application.authors import authors
from application.words.models import Words
from application.poems.models import Poem
from application.poets.models import Poet
from application.poets.models import poet_poem
from application.poets import poets
from application.admin.forms import CreateForm
import itertools
import os, os.path

# Admin dashboard.


@app.before_request
def before_request():
	g.user = current_user


#----------------------------------------------------
#		LIST: users_list()
#----------------------------------------------------
@app.route("/admin", methods=["GET", "POST"])
@login_required(roles=[1])
def admin_dashboard():

	if request.method == "POST":
		users = User.query.all()
		return render_template("admin/dashboard.html", users=users)


#----------------------------------------------------
#		DELETE: user_delete()
#----------------------------------------------------
@app.route("/admin/delete/<user_id>", methods=["POST"])
@login_required(roles=[1])
def user_delete(user_id):

	user_qry = db.session().query(User).filter(User.id==user_id)

	if request.method == "POST":
		try:
			db.session().delete(user_qry.first())
			db.session().commit()
		except SQLAlchemyError:
			db.session.rollback()
			flash("User not deleted.", "danger")

	return render_template("admin/dashboard.html", users = User.query.all())


#----------------------------------------------------
#		CHANGE ADMIN STATUS user_adminate()
#----------------------------------------------------
@app.route("/admin/status/<user_id>", methods=["POST"])
@login_required(roles=[1])
def user_adminate(user_id):

	user_qry = db.session().query(User).filter(User.id==user_id)

	form = CreateForm(request.form)
	if request.form.get("userate") == "userate":
		if int(user_id) != g.user.id:
			user_qry.first().role = 3
			try:
				db.session().commit()
			except SQLAlchemyError:
				db.session.rollback()
				flash("User's status not changed.", "danger")
	elif request.form.get("adminate") == "adminate":
		if user_qry.first().role not in [1,2]:
			user_qry.first().role = 1
			try:
				db.session().commit()
			except SQLAlchemyError:
				db.session.rollback()
				flash("User's status not changed.", "danger")

	return render_template("admin/dashboard.html", users = User.query.all())


#----------------------------------------------------
# Table operations: add default songs, authors
#----------------------------------------------------
@app.route("/defaults/addsongs", methods = ["POST"])
@login_required(roles=[1])
def add_songs():

	if db.session.query(Song).count() > 0 and db.session.query(Author).count() > 0:
		flash("Song database is not empty - cannot add default songs.", "warning")
		return redirect(url_for("auth_stats", load='na'))
	else:
		progress_songs()

	db_poems_status=Poem.find_database_poems_status()
	poem_count = db.session.query(Poem).count()

	if poem_count > 0:
		return render_template("auth/stats.html", db_songs_status=None, db_poems_status=db_poems_status, top_words=None, load='song')
	else:
		return render_template("auth/stats.html", db_songs_status=None, db_poems_status=None, top_words=None, load='song')

#----------------------------------------------------
# Table operations: add default songs, authors
#----------------------------------------------------
@app.route("/progress_songs")
@login_required(roles=[1])
def progress_songs():

	x = 0.0

	num_authors = len(authors.authors)

	document_dir = os.getcwd()+'/application/static/default_songs/'
	lang_list = os.listdir(document_dir)
	num_songs = 0
	for item in lang_list:
		author_songs = os.listdir(document_dir+'/'+item)
		num_songs = num_songs + len(author_songs)

	num_all = num_authors + num_songs

	def generate(x):	#------------------------------------------------
	# add default authors
	#------------------------------------------------
		for auth in authors.authors:
			db.session.add(Author(name=auth,result_all=None,result_no_stop_words=None))
			db.session.commit()
			x = x + 100.0/num_all
			yield "data:" + str('%.4f'%(x)) + "\n\n"

		#------------------------------------------------
		# add default songs
		#------------------------------------------------
		# finnish songs
		for i in range(1,7):
			document_path = os.getcwd()+'/application/static/default_songs/fi/'+str(i)+'.txt'
			file = open(document_path, 'r', encoding='utf-8')
			name = file.readline().rstrip()
			file.close()
			lyrics = ""
			with open(document_path, encoding='utf-8') as f:
				for line in itertools.islice(f, 2, None):
					lyrics += line
			language = 'finnish'
	
			song = Song(name,lyrics,language)
			song.account_id = 1
			song.account_role = 1
		
			if i == 1:
				song.authors.extend([db.session.query(Author).filter(Author.name=='Jens Nicolai Ludvig Schjörring').first(),db.session.query(Author).filter(Author.name=='H. S. Thompson').first()])
			elif i == 2:
				song.authors.extend([db.session.query(Author).filter(Author.name=='Abraham Achrenius').first(),db.session.query(Author).filter(Author.name=='Toisinto Ylistarosta').first()])
			elif i == 3:
				song.authors.extend([db.session.query(Author).filter(Author.name=='Lina Sandell-Berg').first(),db.session.query(Author).filter(Author.name=='Gunr Wennerberg').first()])
			elif i == 4:
				song.authors.extend([db.session.query(Author).filter(Author.name=='Georgiana M. Taylor').first(),db.session.query(Author).filter(Author.name=='Tuntematon').first()])
			elif i == 5:
				song.authors.extend([db.session.query(Author).filter(Author.name=='Johnson Jr. Oatman').first(),db.session.query(Author).filter(Author.name=='Edwin O. Excell').first()])
			elif i == 6:
				song.authors.extend([db.session.query(Author).filter(Author.name=='Tuntematon').first(),db.session.query(Author).filter(Author.name=='Lewis Hartsoug').first()])
	
			try:
				db.session.add(song)
				db.session.commit()
			except:
				db.session.rollback()
	
			x = x + 100.0/num_all
			yield "data:" + str('%.4f'%(x)) + "\n\n"
	
		# english songs
		for i in range(7,13):
			document_path = os.getcwd()+'/application/static/default_songs/en/'+str(i)+'.txt'
			file = open(document_path, 'r', encoding='utf-8')
			name = file.readline().rstrip()
			file.close()
			lyrics = ""
			with open(document_path, encoding='utf-8') as f:
				for line in itertools.islice(f, 2, None):
					lyrics += line
			language = 'english'
	
			song = Song(name,lyrics,language)
			song.account_id = 1
			song.account_role = 1
		
			if i == 7:
				song.authors.extend([db.session.query(Author).filter(Author.name=='Chris Tomlin').first()])
			elif i == 8:
				song.authors.extend([db.session.query(Author).filter(Author.name=='George Crawford Hugg').first(),db.session.query(Author).filter(Author.name=='Johnson Jr. Oatman').first()])
			elif i == 9:
				song.authors.extend([db.session.query(Author).filter(Author.name=='Philip Paul Bliss').first()])
			elif i == 10:
				song.authors.extend([db.session.query(Author).filter(Author.name=='Chris Tomlin').first(),db.session.query(Author).filter(Author.name=='Ed Cash').first(),db.session.query(Author).filter(Author.name=='Stephan Conley Sharp').first()])
			elif i == 11:
				song.authors.extend([db.session.query(Author).filter(Author.name=='Matt Maher').first()])
			elif i == 12:
				song.authors.extend([db.session.query(Author).filter(Author.name=='Hillsong United').first()])
	
			try:
				db.session.add(song)
				db.session.commit()
			except:
				db.session.rollback()
	
			x = x + 100.0/num_all
			yield "data:" + str('%.4f'%(x)) + "\n\n"
	
		# french songs
		for i in range(13,19):
			document_path = os.getcwd()+'/application/static/default_songs/fr/'+str(i)+'.txt'
			file = open(document_path, 'r', encoding='utf-8')
			name = file.readline().rstrip()
			file.close()
			lyrics = ""
			with open(document_path, encoding='utf-8') as f:
				for line in itertools.islice(f, 2, None):
					lyrics += line
			language = 'french'
	
			song = Song(name,lyrics,language)
			song.account_id = 1
			song.account_role = 1
		
			if i == 13:
				song.authors.extend([db.session.query(Author).filter(Author.name=='John van den Hogen').first()])
			elif i == 14:
				song.authors.extend([db.session.query(Author).filter(Author.name=='Mlle Amélie Humbert').first(),db.session.query(Author).filter(Author.name=='George Coles Stebbins').first()])
			elif i == 15:
				song.authors.extend([db.session.query(Author).filter(Author.name=='Charles Rochedieu').first(),db.session.query(Author).filter(Author.name=='William Herbert Jude').first()])
			elif i == 16:
				song.authors.extend([db.session.query(Author).filter(Author.name=='Mlle Amélie Humbert').first(),db.session.query(Author).filter(Author.name=='C.-C. Williams').first()])
			elif i == 17:
				song.authors.extend([db.session.query(Author).filter(Author.name=='Horatio Richmond Palmer').first()])
			elif i == 18:
				song.authors.extend([db.session.query(Author).filter(Author.name=='Jean-François Bussy').first()])
	
			try:
				db.session.add(song)
				db.session.commit()
			except:
				db.session.rollback()
	
			x = x + 100.0/num_all
			yield "data:" + str('%.4f'%(x)) + "\n\n"

	return Response(generate(x), mimetype= 'text/event-stream')


#----------------------------------------------------
# Table operations: remove default songs, authors, results
#----------------------------------------------------
@app.route("/defaults/removesongs", methods = ["POST"])
@login_required(roles=[1])
def remove_songs():
		
	if db.session.query(Song).count() == 0 and db.session.query(Author).count() == 0:
		flash("Authors and Songs already empty.", "warning")
	else:
		try:
			db.session.query(Song).delete()
			db.session.commit()
		except:
			flash("Table Song not cleared.", "danger")
			db.session.rollback()
		
		try:
			db.session.query(Author).delete()
			db.session.commit()
		except:
			flash("Table Author not cleared.", "danger")
			db.session.rollback()
		
		try:
			db.session.query(Words).delete()
			db.session.commit()
		except:
			flash("Table Words not cleared.", "danger")
			db.session.rollback()
	
		try:
			stmt = text("DELETE FROM author_song;")
			db.engine.execute(stmt)
		except:
			flash("Join table author_song not cleared.", "danger")
			db.session.rollback()
		
		try:
			stmt = text("DELETE FROM song_result;")
			db.engine.execute(stmt)
		except:
			flash("Join table song_result not cleared.", "danger")
			db.session.rollback()

		flash("Tables cleared.", "success")

	db_poems_status=Poem.find_database_poems_status()
	poem_count = db.session.query(Poem).count()

	return redirect(url_for("auth_stats", load='na'))


#----------------------------------------------------
# Table operations: add default poets, poems
#----------------------------------------------------
@app.route("/defaults/addpoems", methods = ["POST"])
@login_required(roles=[1])
def add_poems():

	if db.session.query(Poet).count() > 0 and db.session.query(Poem).count() > 0:
		flash("Poem database is not empty - cannot add default poems.", "warning")
		return redirect(url_for("auth_stats", load='na'))
	else:
		progress_poems()

	db_songs_status=Song.find_database_songs_status()
	song_count = db.session.query(Song).count()

	if song_count > 0:
		return render_template("auth/stats.html", db_songs_status=db_songs_status, db_poems_status=None, top_words=None, load='poem')
	else:
		return render_template("auth/stats.html", db_songs_status=None, db_poems_status=None, top_words=None, load='poem')


#----------------------------------------------------
# Table operations: add default poets, poems
#----------------------------------------------------
@app.route("/progress_poems")
@login_required(roles=[1])
def progress_poems():

	x = 0.0

	num_poets = len(poets.poets_fi) + len(poets.poets_en) + len(poets.poets_fr)

	document_dir = os.getcwd()+'/application/static/default_poems/'
	lang_list = os.listdir(document_dir)
	num_poems = 0
	for item in lang_list:
		poet_list = os.listdir(document_dir+'/'+item)
		for i in poet_list:
			poet_poems = os.listdir(document_dir+'/'+item+'/'+i)
			num_poems = num_poems + len(poet_poems)

	num_all = num_poets + num_poems

	def generate(x):
		#------------------------------------------------
		# add default authors
		#------------------------------------------------
		for item in poets.poets_fi:
			db.session.add(Poet(name=item,result_all=None,result_no_stop_words=None))
			db.session.commit()
			x = x + 100.0/num_all
			yield "data:" + str('%.4f'%(x)) + "\n\n"
		for item in poets.poets_en:
			db.session.add(Poet(name=item,result_all=None,result_no_stop_words=None))
			db.session.commit()
			x = x + 100.0/num_all
			yield "data:" + str('%.4f'%(x)) + "\n\n"
		for item in poets.poets_fr:
			db.session.add(Poet(name=item,result_all=None,result_no_stop_words=None))
			db.session.commit()
			x = x + 100.0/num_all
			yield "data:" + str('%.4f'%(x)) + "\n\n"

		#------------------------------------------------
		# add default poems
		#------------------------------------------------
		# finnish poems
		#------------------------------------------------
		for i in range(1,61):
			document_path = document_dir + 'fi/uuno_kailas/'+str(i)+'.txt'
			file = open(document_path, 'r', encoding='utf-8')
			name = file.readline().rstrip()
			file.close()
			lyrics = ""
			with open(document_path, encoding='utf-8') as f:
				for line in itertools.islice(f, 1, None):
					lyrics += line
			language = 'finnish'
		
			poem = Poem(name,lyrics,language)
			poem.account_id = 1
			poem.account_role = 1
		
			poem.poets.extend(db.session.query(Poet).filter(Poet.name=='Uuno Kailas'))
		
			try:
				db.session.add(poem)
				db.session.commit()
			except:
				db.session.rollback()

			x = x + 100.0/num_all
			yield "data:" + str('%.4f'%(x)) + "\n\n"
		
		for i in range(1,78):
			document_path = document_dir + 'fi/edith_sodergran/'+str(i)+'.txt'
			file = open(document_path, 'r', encoding='utf-8')
			name = file.readline().rstrip()
			file.close()
			lyrics = ""
			with open(document_path, encoding='utf-8') as f:
				for line in itertools.islice(f, 1, None):
					lyrics += line
			language = 'finnish'
		
			poem = Poem(name,lyrics,language)
			poem.account_id = 1
			poem.account_role = 1
		
			poem.poets.extend(db.session.query(Poet).filter(Poet.name=='Edith Södergran'))
		
			try:
				db.session.add(poem)
				db.session.commit()
			except:
				db.session.rollback()

			x = x + 100.0/num_all
			yield "data:" + str('%.4f'%(x)) + "\n\n"
		
		
		#------------------------------------------------
		# english poems
		#------------------------------------------------
		for i in range(1,50):
			document_path = document_dir + 'en/edgar_allan_poe/'+str(i)+'.txt'
			file = open(document_path, 'r', encoding='utf-8')
			name = file.readline().rstrip()
			file.close()
			lyrics = ""
			with open(document_path, encoding='utf-8') as f:
				for line in itertools.islice(f, 1, None):
					lyrics += line
			language = 'english'
		
			poem = Poem(name,lyrics,language)
			poem.account_id = 1
			poem.account_role = 1
		
			poem.poets.extend(db.session.query(Poet).filter(Poet.name=='Edgar Allan Poe'))
		
			try:
				db.session.add(poem)
				db.session.commit()
			except:
				db.session.rollback()

			x = x + 100.0/num_all
			yield "data:" + str('%.4f'%(x)) + "\n\n"
		
		
		for i in range(1,46):
			document_path = document_dir + 'en/emily_dickinson/'+str(i)+'.txt'
			file = open(document_path, 'r', encoding='utf-8')
			name = file.readline().rstrip()
			file.close()
			lyrics = ""
			with open(document_path, encoding='utf-8') as f:
				for line in itertools.islice(f, 1, None):
					lyrics += line
			language = 'english'
		
			poem = Poem(name,lyrics,language)
			poem.account_id = 1
			poem.account_role = 1
		
			poem.poets.extend(db.session.query(Poet).filter(Poet.name=='Emily Dickinson'))
		
			try:
				db.session.add(poem)
				db.session.commit()
			except:
				db.session.rollback()

			x = x + 100.0/num_all
			yield "data:" + str('%.4f'%(x)) + "\n\n"
		
		
		#------------------------------------------------
		# french poems
		#------------------------------------------------
		for i in range(1,105):
			document_path = document_dir + 'fr/charles_baudelaire/'+str(i)+'.txt'
			file = open(document_path, 'r', encoding='utf-8')
			name = file.readline().rstrip()
			file.close()
			lyrics = ""
			with open(document_path, encoding='utf-8') as f:
				for line in itertools.islice(f, 1, None):
					lyrics += line
			language = 'french'
		
			poem = Poem(name,lyrics,language)
			poem.account_id = 1
			poem.account_role = 1
		
			poem.poets.extend(db.session.query(Poet).filter(Poet.name=='Charles Baudelaire'))
		
			try:
				db.session.add(poem)
				db.session.commit()
			except:
				db.session.rollback()

			x = x + 100.0/num_all
			yield "data:" + str('%.4f'%(x)) + "\n\n"
		
		
		for i in range(1,44):
			document_path = document_dir + 'fr/louise_ackermann/'+str(i)+'.txt'
			file = open(document_path, 'r', encoding='utf-8')
			name = file.readline().rstrip()
			file.close()
			lyrics = ""
			with open(document_path, encoding='utf-8') as f:
				for line in itertools.islice(f, 1, None):
					lyrics += line
			language = 'french'
		
			poem = Poem(name,lyrics,language)
			poem.account_id = 1
			poem.account_role = 1
		
			poem.poets.extend(db.session.query(Poet).filter(Poet.name=='Louise Ackermann'))
		
			try:
				db.session.add(poem)
				db.session.commit()
			except:
				db.session.rollback()

			x = x + 100.0/num_all
			yield "data:" + str('%.4f'%(x)) + "\n\n"

	return Response(generate(x), mimetype= 'text/event-stream')


#----------------------------------------------------
# Table operations: remove default poets, poems
#----------------------------------------------------
@app.route("/defaults/removepoems", methods = ["POST"])
@login_required(roles=[1])
def remove_poems():

	if db.session.query(Poet).count() == 0 and db.session.query(Poem).count() == 0:
		flash("Poets and Poems already empty.", "warning")
	else:
		try:
			db.session.query(Poem).delete()
			db.session.commit()
		except:
			flash("Table Poem not cleared.", "danger")
			db.session.rollback()
			
		try:
			db.session.query(Poet).delete()
			db.session.commit()
		except:
			flash("Table Poet not cleared.", "danger")
			db.session.rollback()
	
		try:
			stmt = text("DELETE FROM poet_poem;")
			db.engine.execute(stmt)
		except:
			flash("Join table poet_poem not cleared.", "danger")
			db.session.rollback()

		flash("Tables Poet, Poem, and poet_poem cleared.", "success")

	return redirect(url_for("auth_stats", load='na'))
