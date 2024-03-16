import re
from app import myApp
from flask import request, make_response, render_template, abort, redirect, url_for, session
import random
from main.forms import SimpleForm
from models import Role, User

@myApp.route("/")
def inf():
    return render_template('index.html')
@myApp.route("/index")
def index():
    session_text = session.get('data')
    if session_text is not None and session_text != "":
        return render_template("index.html", auth = session.get("auth"), username=session_text["username"],password=session_text["password"],
                               email=session_text["email"],gender=session_text["gender"])
    else:
        return render_template('index.html', auth = session.get("auth"))

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
        user = User.query.filter_by(username = form.username.data, password = form.password.data, email = form.email.data, gender = form.gender.data).first()
        if user is not None:
            data = form.data
            session["data"] = {"username": data["username"], "password": data["password"], "email": data["email"], "gender": data["gender"]}
            form.username.data = ''
            form.password.data = ''
            form.email.data = ''
            session["auth"] = True
        else:
            session["auth"] = False
        return redirect(url_for('index'))
    return render_template('formtemplate.html', form=form, auth = session.get("auth"))

@myApp.route("/logout")
def logout():
    if session.get("auth"):
        session["auth"] = False
    return redirect(url_for('index'))





'''
@myApp.route("/testForm", methods = ["GET","POST"])
def testform():
    form = SimpleForm()
    if form.validate_on_submit():
        data = form.data
        session["data"] = {"username": data["username"], "email": data["email"], "password": data["password"], "gender": data["gender"]}
        form.login.data = ''
        form.email.data = ''
        form.password.data = ''
        form.confirm_password.data = ''
        return redirect(url_for('index'))
    return render_template('formtemplate.html', form=form)
'''