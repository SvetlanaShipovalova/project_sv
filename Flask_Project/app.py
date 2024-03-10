from flask import Flask
from flask_bootstrap import Bootstrap5

myApp = Flask(__name__)
myApp.config["SECRET_KEY"] = "hard to unlock"
bootstrap = Bootstrap5(myApp)

from main import forms
from main import routes