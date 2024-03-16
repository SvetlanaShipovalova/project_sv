import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask import Flask
from flask_bootstrap import Bootstrap5

basedir = os.path.abspath(os.path.dirname(__file__))
myApp = Flask(__name__)

myApp.config["SECRET_KEY"] = "hard to unlock"
myApp.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/flask_project"
myApp.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(myApp)
migrate = Migrate(myApp, db)

bootstrap = Bootstrap5(myApp)

from main import forms
from main import routes








