import re
from app import myApp
from flask import request, make_response, render_template, abort, redirect, url_for, session
import random
from main.forms import SimpleForm


class User:
    def __init__(self, id_user, name):
        self.id_user = id_user
        self.name = name

def load_user(user_id):
    if user_id == "14":
        return User(14,"Светлана")
    elif user_id == "36":
        return User(36,"Кристина")
    else:
        return None
@myApp.route("/")
def inf():
    return render_template('index.html')
@myApp.route("/index")
def index():
    user = {"username": "Петя"}
    user_agent = request.headers.get('user-agent')
    session_text = session.get('data')
    if session_text is not None and session_text != "":
        return render_template("index.html", user=user,email=session_text["email"], gender=session_text["gender"], login=session_text["login"], password=session_text["password"])
    else:
        return render_template('index.html', user=user)

"""5
@myApp.route("/user/<name>")
def hello_user(name):
    return "<h2>Good day, {}<h2>".format(name)
"""
@myApp.route("/bad_request")
def bad_fill(code=400):
    abort(400)
    return "<h3>Bad Request<h3>", code

@myApp.route("/custom_response")
def cust_response():
    browser = request.user_agent
    browser = re.search("Firefox", str(browser))
    if browser is not None:
        browser_name = browser.group(0).format()
        flag = str(random.randint(1000, 9999))
        response = make_response("<h1>Put this in cookie!</h1>")
        response.set_cookie("answer", flag)
    else:
        response = make_response('<h1>Not using Mozilla browser</h1>')
    return response

@myApp.route("/user/<user_id>")
def get_user(user_id):
    user = load_user(user_id)
    if user is None:
        return bad_fill(404)
    else:
        return "<h2>Hi, {}<h2>".format(user.name)

@myApp.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@myApp.errorhandler(400)
def page_not(e):
    return render_template("400.html"), 400

myApp.add_url_rule("/","index",index)

@myApp.route("/testForm", methods = ["GET","POST"])
def testform():
    form = SimpleForm()
    if form.validate_on_submit():
        data = form.data
        session["data"] = {"login": data["login"], "email": data["email"], "password": data["password"], "gender": data["gender"]}
        form.login.data = ''
        form.email.data = ''
        form.password.data = ''
        form.confirm_password.data = ''
        return redirect(url_for('index'))
    return render_template('formtemplate.html', form=form)
