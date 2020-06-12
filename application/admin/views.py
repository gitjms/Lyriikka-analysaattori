from flask import url_for, redirect, render_template, request, flash, g
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
import os

# Admin dashboard.


@app.before_request
def before_request():
	g.user = current_user


#----------------------------------------------------
#		LIST: users_list()
#----------------------------------------------------
@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin_dashboard():

	if g.user.role != "ADMIN":
		return login_manager.unauthorized()

	if request.method == "GET":
		return render_template("auth/stats.html")

	if request.method == "POST":
		return render_template("admin/dashboard.html", users = User.query.all())


#----------------------------------------------------
#		DELETE: user_delete()
#----------------------------------------------------
@app.route("/admin/delete/<user_id>", methods=["POST"])
@login_required
def user_delete(user_id):

	if g.user.role != "ADMIN":
		return login_manager.unauthorized()

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
@login_required
def user_adminate(user_id):

	if g.user.role != "ADMIN":
		return login_manager.unauthorized()

	user_qry = db.session().query(User).filter(User.id==user_id)

	form = CreateForm(request.form)
	if request.form.get("userate") == "userate":
		if user_qry.first().role not in ["ADMIN","GUEST"]:
			user_qry.first().role = "USER"
	elif request.form.get("adminate") == "adminate":
		if user_qry.first().role not in ["ADMIN","GUEST"]:
			user_qry.first().role = "ADMIN"

	if request.method == "POST":
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
@login_required
def add_songs():

	if g.user.role != "ADMIN":
		return login_manager.unauthorized()

	#------------------------------------------------
	# add default authors
	#------------------------------------------------

	if db.session.query(Song).count() > 0:
		flash("Default songs and authors already exist.", "warning")
		return redirect(url_for("auth_stats"))

	for item in authors.authors_fi:
		for auth in item[0]:
			db.session.add(Author(name=auth,result_all=None,result_no_stop_words=None))
			db.session.commit()

	for item in authors.authors_en:
		for auth in item[0]:
			db.session.add(Author(name=auth,result_all=None,result_no_stop_words=None))
			db.session.commit()
	
	for item in authors.authors_fr:
		for auth in item[0]:
			db.session.add(Author(name=auth,result_all=None,result_no_stop_words=None))
			db.session.commit()

	#------------------------------------------------
	# add default songs
	#------------------------------------------------

	fi_added = False
	en_added = False
	fr_added = False

	# finnish songs
	for i in range(1,7):
		document_path = os.getcwd()+'/application/static/default_songs/fi/song'+str(i)+'.txt'
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
			fi_added = True
		except:
			db.session.rollback()

	# english songs
	for i in range(7,13):
		document_path = os.getcwd()+'/application/static/default_songs/en/song'+str(i)+'.txt'
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
			en_added = True
		except:
			db.session.rollback()

	# french songs
	for i in range(13,19):
		document_path = os.getcwd()+'/application/static/default_songs/fr/song'+str(i)+'.txt'
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
			fr_added = True
		except:
			db.session.rollback()

	if fi_added:
		flash("Finnish songs added.", "success")
	else:
		flash("Finnish songs not added.", "danger")
	if en_added:
		flash("English songs added.", "success")
	else:
		flash("English songs not added.", "danger")
	if fr_added:
		flash("French songs added.", "success")
	else:
		flash("French songs not added.", "danger")
	
	
	return redirect(url_for("auth_stats"))


#----------------------------------------------------
# Table operations: remove default songs, authors, results
#----------------------------------------------------
@app.route("/defaults/removesongs", methods = ["POST"])
@login_required
def remove_songs():

	if g.user.role != "ADMIN":
		return login_manager.unauthorized()
		
	try:
		db.session.query(Song).delete()
		db.session.commit()
		flash("Table Song cleared.", "success")
	except:
		flash("Table Song not cleared.", "danger")
		db.session.rollback()
	
	try:
		db.session.query(Author).delete()
		db.session.commit()
		flash("Table Author cleared.", "success")
	except:
		flash("Table Author not cleared.", "danger")
		db.session.rollback()
	
	try:
		db.session.query(Words).delete()
		db.session.commit()
		flash("Table Words cleared.", "success")
	except:
		flash("Table Words not cleared.", "danger")
		db.session.rollback()

	try:
		stmt = text("DELETE FROM author_song;")
		db.engine.execute(stmt)
		flash("Join table author_song cleared.", "success")
	except:
		flash("Join table author_song not cleared.", "danger")
		db.session.rollback()
		
	try:
		stmt = text("DELETE FROM song_result;")
		db.engine.execute(stmt)
		flash("Join table song_result cleared.", "success")
	except:
		flash("Join table song_result not cleared.", "danger")
		db.session.rollback()

	return redirect(url_for("auth_stats"))


#----------------------------------------------------
# Table operations: add default poets, poems
#----------------------------------------------------
@app.route("/defaults/addpoems", methods = ["POST"])
@login_required
def add_poems():

	if g.user.role != "ADMIN":
		return login_manager.unauthorized()

	#------------------------------------------------
	# add default authors
	#------------------------------------------------

	if db.session.query(Poet).count() > 0:
		flash("Default poets already exist.", "warning")

	for item in poets.poets_fi:
		db.session.add(Poet(name=item[0],result_all=None,result_no_stop_words=None))
		db.session.commit()

	for item in poets.poets_en:
		db.session.add(Poet(name=item[0],result_all=None,result_no_stop_words=None))
		db.session.commit()
	
	for item in poets.poets_fr:
		db.session.add(Poet(name=item[0],result_all=None,result_no_stop_words=None))
		db.session.commit()

	#------------------------------------------------
	# add default poems
	#------------------------------------------------

	if db.session.query(Poem).count() > 0:
		flash("Default poems already exist.", "warning")
		return redirect(url_for("auth_stats"))

	fi_added = False
	en_added = False
	fr_added = False

	# finnish poems
	for i in range(1,31):
		document_path = os.getcwd()+'/application/static/default_poems/fi/uuno_kailas/poem'+str(i)+'.txt'
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
	
		poem.poets.extend(db.session.query(Poet).filter(Poet.name=='Uuno Kailas'))

		try:
			db.session.add(poem)
			db.session.commit()
			fi_added = True
		except:
			db.session.rollback()

	# english poems
	for i in range(31,61):
		document_path = os.getcwd()+'/application/static/default_poems/en/edgar_allan_poe/poem'+str(i)+'.txt'
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
	
		poem.poets.extend(db.session.query(Poet).filter(Poet.name=='Edgar Allan Poe'))

		try:
			db.session.add(poem)
			db.session.commit()
			en_added = True
		except:
			db.session.rollback()

	# french poems
	for i in range(61,91):
		document_path = os.getcwd()+'/application/static/default_poems/fr/charles_baudelaire/poem'+str(i)+'.txt'
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
	
		poem.poets.extend(db.session.query(Poet).filter(Poet.name=='Charles Baudelaire'))

		try:
			db.session.add(poem)
			db.session.commit()
			fr_added = True
		except:
			db.session.rollback()

	if fi_added:
		flash("Finnish poems added.", "success")
	else:
		flash("Finnish poems not added.", "danger")
	if en_added:
		flash("English poems added.", "success")
	else:
		flash("English poems not added.", "danger")
	if fr_added:
		flash("French poems added.", "success")
	else:
		flash("French poems not added.", "danger")
	
	
	return redirect(url_for("auth_stats"))


#----------------------------------------------------
# Table operations: remove default poets, poems
#----------------------------------------------------
@app.route("/defaults/removepoems", methods = ["POST"])
@login_required
def remove_poems():

	if g.user.role != "ADMIN":
		return login_manager.unauthorized()

	try:
		db.session.query(Poem).delete()
		db.session.commit()
		flash("Table Poem cleared.", "success")
	except:
		flash("Table Poem not cleared.", "danger")
		db.session.rollback()
		
	try:
		db.session.query(Poet).delete()
		db.session.commit()
		flash("Table Poet cleared.", "success")
	except:
		flash("Table Poet not cleared.", "danger")
		db.session.rollback()

	try:
		stmt = text("DELETE FROM poet_poem;")
		db.engine.execute(stmt)
		flash("Join table poet_poem cleared.", "success")
	except:
		flash("Join table poet_poem not cleared.", "danger")
		db.session.rollback()

	return redirect(url_for("auth_stats"))
