#Importation of relevant modules needed

from application import db, login_manager
from flask_login import UserMixin
from datetime import datetime

'''database model for the table 'Notes', user_id is the foreign key which links
the student users table'''
class Notes(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False, unique=True)
	content = db.Column(db.String(10000), nullable=False, unique=True)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('student_users.id'), nullable=False)

	def __repr__(self): #hidden method that returns a printable representation of an object
		return ''.join(['User ID : ', self.user_id, '\r\n' 'Title: ', self.title, '\r\n', self.content])

'''database model for the table 'StudentUsers', uni_id, soc_id are the foreign keys which links
the univeristy and society table respectively'''
class StudentUsers(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(30), nullable=False)
	last_name = db.Column(db.String(30), nullable=False)
	uni_name = db.Column(db.String(30), nullable=False)
	email = db.Column(db.String(150), nullable=False, unique=True)
	password = db.Column(db.String(50), nullable=False)
	uni_id = db.Column(db.Integer, db.ForeignKey('university.id'), nullable=False)
	soc_id = db.Column(db.Integer, db.ForeignKey('society.id'), nullable=True)
	soc_name = db.Column(db.String(50), nullable=True)
	note = db.relationship('Notes', backref='mine', lazy=True)

	def __repr__(self): #hidden method that returns a printable representation of an object
		return ''.join(['User ID: ', str(self.id), '\r\n', 
			'Email: ', self.email, '\r\n',
			'Name: ', self.first_name, '', self.last_name, '\r\n', 'University: ', self.uni_name])

'''database model for the table 'StudentUsers', uni_id, soc_id are the foreign keys which links
the univeristy and society table respectively'''
class University(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	uni_name = db.Column(db.String(30))
	uni = db.relationship('StudentUsers', backref='user', lazy=True)
	uni_s = db.relationship('Society', backref='author', lazy=True)
	
	def __repr__(self): #hidden method that returns a printable representation of an object
		return ''.join(['Uni_ID: ', str(self.id), '\r\n',
			'UNI: ', self.uni_name])

'''database model for the table 'Society'''
class Society(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	SocietyName = db.Column(db.String(200))
	About = db.Column(db.String(10000))
	uni_id = db.Column(db.Integer, db.ForeignKey('university.id'), nullable=False)
	soc = db.relationship('StudentUsers', backref='creator', lazy=True)

	def __repr__(self): #hidden method that returns a printable representation of an object
		return ''.join(['UNI ID: ', str(self.id)])

@login_manager.user_loader ######
def load_user(id):
	return StudentUsers.query.get(int(id))
