from flask import url_for, redirect, render_template, request, flash, g
from flask_login import current_user

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.sql import func, text

from application import app, db, login_manager, login_required
from application.auth.views import find_database_status
from application.auth.models import User
from application.songs.models import Song
from application.authors.models import Author
from application.authors.models import author_song
from application.words.models import Words
from application.authors import authors
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
		return render_template("auth/home.html", db_status=find_database_status())

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
		user_qry.first().role = "USER"
	elif request.form.get("adminate") == "adminate":
		user_qry.first().role = "ADMIN"

	if request.method == "POST":
		try:
			db.session().commit()
		except SQLAlchemyError:
			db.session.rollback()
			flash("User's status not changed.", "danger")

	return render_template("admin/dashboard.html", users = User.query.all())


#----------------------------------------------------
# Table operations: remove default songs & authors
#----------------------------------------------------
@app.route("/defaults/remove", methods = ["POST"])
@login_required
def remove_songs():

	if g.user.role != "ADMIN":
		return login_manager.unauthorized()

	#----------------------------------------------------
	# Remove default authors and songs
	#----------------------------------------------------
	if request.form.get('remove') == "remove":
		
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
			stmt = text("DELETE FROM author_song;")
			db.engine.execute(stmt)
			flash("Join table author_song cleared.", "success")
		except:
			flash("Join table author_song not cleared.", "danger")
			db.session.rollback()
			flash("Tables not cleared.", "danger")

		try:
			stmt = text("DELETE FROM song_result;")
			db.engine.execute(stmt)
			flash("Join table song_result cleared.", "success")
		except:
			flash("Join table song_result not cleared.", "danger")
			db.session.rollback()
			flash("Tables not cleared.", "danger")
		
		db.drop_all(bind=None)
		db.create_all()
		flash("Tables cleared.", "success")

	return render_template("auth/home.html", db_status=None, top_words=None)


#----------------------------------------------------
# Table operations: add default songs & authors
#----------------------------------------------------
@app.route("/defaults/add", methods = ["POST"])
@login_required
def add_songs():

	if g.user.role != "ADMIN":
		return login_manager.unauthorized()

	#----------------------------------------------------
	# Add default authors and songs
	#----------------------------------------------------

	if request.form.get('add') == "add":

		#------------------------------------------------
		# add default authors
		#------------------------------------------------

		db_status=find_database_status
		if not db_status:
			flash("Default authors already exist.", "warning")
			return render_template("auth/home.html", db_status=None, top_words=None)
		else:
			for item in authors.authors_fi:
				song = item[1]
				for auth in item[0]:
					db.session.add(Author(name=auth))
					db.session.commit()

			for item in authors.authors_en:
				song = item[1]
				for auth in item[0]:
					db.session.add(Author(name=auth))
					db.session.commit()
			
			for item in authors.authors_fr:
				song = item[1]
				for auth in item[0]:
					db.session.add(Author(name=auth))
					db.session.commit()

		#------------------------------------------------
		# add default songs
		#------------------------------------------------

		fi_added = False
		en_added = False
		fr_added = False

		db_status=find_database_status
		if not db_status:
			flash("Default Songs already exist.", "warning")
			return render_template("auth/home.html", db_status=None, top_words=None)
		else:
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
	
	
	return redirect(url_for("songs_home"))
