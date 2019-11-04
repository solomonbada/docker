#Importation of relevant modules needed

from flask import render_template, url_for, redirect, request
from application import app, db, bcrypt
from application.models import StudentUsers, Society, University, Notes
from application.forms import StudentRegistrationForm, StudentLoginForm, UpdateAccountForm, NotesForm
from flask_login import login_user, current_user, logout_user, login_required
from wtforms_sqlalchemy.fields import QuerySelectField
import sqlite3

#url route that directs the user to the home/landing page
@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html', title='Home') #function renders the code written in home.html with the title as 'Home'

#url route that directs the user to the about page
@app.route('/about')
def about():
	#function renders the code written in about.html with the title as 'About'
    return render_template('about.html', title='About')

#url route that directs the user to the register page
@app.route('/register', methods=['GET', 'POST'])
def register(): 
	if current_user.is_authenticated:
		return redirect(url_for('mytimeline'))	
	form = StudentRegistrationForm() #Grabs the StudentRegistration form from applications.forms.py
	if form.validate_on_submit(): ####
		hashed_password = bcrypt.generate_password_hash(form.password.data) #Generates a hashed form of the password within the database
		user = StudentUsers(first_name=form.first_name.data.capitalize(), last_name=form.last_name.data.capitalize(), uni_id=form.uni_id.data, uni_name=form.uni_name.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit() #adds all the information submitted by the user to the database to be stored
		return redirect(url_for('login')) #after registration, the user is redirected to the login page
	return render_template('register.html', title='Register', form=form)

#url route that directs the user to the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated: #if the current user is already logged in they should be redirected to the 'mytimeline' page
		return redirect(url_for('mytimeline'))
	else: #if they are not logged in the followiung have to be adhered to
		form = StudentLoginForm()
		if form.validate_on_submit():
			user = StudentUsers.query.filter_by(email=form.email.data).first() #a search query is made to the database to ensure the input email matches cont.
			#one present in the database
			if user and bcrypt.check_password_hash(user.password, form.password.data): #if bother the user email and password match then the user is logged in
				login_user(user, remember=form.remember.data)
				return redirect(url_for('mytimeline')) #user is redirected to the page 'mytimeline'
		return render_template('login.html', title='Login', form=form)

#url route that directs the user to mytimeline page
@app.route('/mytimeline', methods=['GET', 'POST'])
@login_required #to access such page, a login by the user is required
def mytimeline():
	form = NotesForm
	if current_user.is_authenticated: #if statement that enables the user to view 'mytimeline' page if they are logged in
		notes = Notes.query.filter_by(mine=current_user).all()
		return render_template('mytimeline.html', title='My Timeline', notes=notes, mine=current_user, form=form)
	return render_template('mytimeline.html', title='My Timeline', notes=notes, mine=current_user, form=form)
 
#url route that directs the user to the accounts page
@app.route('/account', methods=['GET', 'POST'])
@login_required #to access such page, a login by the user is required
def account():
	form = UpdateAccountForm() #within the function, the form that is to be used is the UpdateAccountForm
	if form.validate_on_submit(): #following block of code allows the user to enter new details to be updated
		current_user.first_name = form.first_name.data.capitalize()
		current_user.last_name = form.last_name.data.capitalize()
		current_user.email = form.email.data
		current_user.soc_name = form.SocietyName.data
		db.session.commit() #commits and saves the changes to the database
		return redirect(url_for('account'))
	elif request.method == 'GET': #GET request displays the current users details in the text boxes 
		form.first_name.data = current_user.first_name
		form.last_name.data = current_user.last_name
		form.email.data = current_user.email
		lists = Society.query.filter_by(uni_id=current_user.uni_id).all() #Queries the database to present results in a dropdown format of all univeristy societies for the current user
		names = []
		for i in range(int(len(lists))):
			temp = [lists[i].SocietyName, lists[i].SocietyName] 
			names.append(temp) #This method adds a the previous item (name) to the existing list of society names
		form.SocietyName.choices=names
	return render_template('account.html', title='Account', form=form, creator=current_user)

#url route that directs the user to the 'viewsocieties' page
@app.route('/viewsocieties')
@login_required #to access such page, a login by the user is required
def viewsocieties():
	if current_user.is_authenticated: #if the current user is aunthenticated, query the society table in the databse, filter by the current user's unii id
		societies = Society.query.filter_by(uni_id=current_user.uni_id)
	return render_template('viewsocieties.html', title='View Societies', societies=societies, creator=current_user)

#url route that directs the the user to view more about the society
@app.route('/viewsocieties/<int(min=1):society_id>')
@login_required
def more(society_id):
	society1 = Society.query.filter_by(id=society_id).first() #queries the society table and filters by the society
	return render_template('more.html', title='More Info', society=society1)

#url route that directs the user to the notes page
@app.route('/notes', methods=['GET', 'POST'])
@login_required
def note():
	form = NotesForm() #within the function, the form that is to be used is the NotesForm
	if form.validate_on_submit():
		postData = Notes(
			title=form.title.data,
			content=form.content.data,
			mine=current_user
			)
		db.session.add(postData)
		db.session.commit() #adds all the information submitted by the user to the database to be stored
		return redirect(url_for('mytimeline')) #redirects the user back to the 'mytimeline' page where they can view their notes
	else:
		print(form.errors)
	return render_template('notes.html', title='Create Note', form=form)

#a route for the deletion of made posts
@app.route("/notes/<int(min=1):note_id>/delete", methods=['POST'])
@login_required
def delete_post(note_id):
	note = Notes.query.filter_by(id=note_id).first() #queiries the database based upon the note id
	db.session.delete(note) #deletes the coressponding note in the databases which is specified by the id
	db.session.commit() #updates the database
	return redirect(url_for('mytimeline')) #redirects the user back to the 'mytimelinepage'

@app.route("/logout")
def logout():
	logout_user() #function which logs out current user
	return redirect(url_for('home')) #redirects to the home page




