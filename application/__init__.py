#Importation of relevant library needed

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
#the secret key is needed to keep the client-side session secure
app.config['SECRET_KEY'] = '6732vbu3d3237bdjbkwqebd239739323'
#An instance of the SQLAlchemy is created to manipulate the SQLite tables by creating a URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#Instance is made by passing the 'app' to SQLAlchemy
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
'''The login manager contains the code that lets your application
and Flask-login work together'''
login_manager = LoginManager(app)
login_manager.login_view = 'login' #the login.html needs to be accessed if the page requires a logged in user

from application import routes
