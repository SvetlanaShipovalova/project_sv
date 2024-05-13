from flask import render_template,  session, abort
from app.models import User, Permission
from . import main
from ..decorators import admin_required, permission_required
from flask_login import login_required


@main.route('/')
@main.route('/index')
def index():
    session_text = session.get('text')
    if session_text is not None or session_text != "":
        return render_template("index.html")
    else:
        return render_template('index.html')

@main.route("/bad_request")
def bad_fill(code=400):
    abort(400)
    return "<h3>Bad Request<h3>", code

'''
@main.route("/testForm", methods = ["GET","POST"])
def testform():
    form = SimpleForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data, password = form.password.data,
                                    email = form.email.data).first()
        if user is not None:
            data = form.data
            session["data"] = {"username": data["username"], "password": data["password"], "email": data["email"]}
            form.username.data = ''
            form.password.data = ''
            form.email.data = ''
            session["auth"] = True
        else:
            session["auth"] = False
        return redirect(url_for('main.index'))
    return render_template('formTemplate.html', form=form, auth = session.get("auth"))


@main.route('/confirm', methods=['POST'])
def confirm():
    user = session.get('data')
    user_email = user["email"]
    send_mail(user_email, "Экспорт данных","send_mail",user=user)
    return redirect(url_for('index'))

def send_mail(to,subject, template, **kwargs):
    html = render_template('send_mail.html', **kwargs)
    msg = Message(subject,
                  sender = main.config["MAIL_USERNAME"],
                  recipients=[to],
                  html=html,
                  )
    mail.send(msg)
'''

@main.route("/secret")
@login_required
def secret():
    print("test login")
    return "Only for auth"

@main.route("/testConfirm")
def testConfirm():
    user = User.query.filter_by().first()
    tmp = user.generate_confirmation_token()
    user.confirm(tmp)

@main.route('/admin')
@login_required
@admin_required
def for_admin():
    return "For admin"

@main.route('/moderate')
@login_required
@permission_required(Permission.DRIVERS)
def for_moderator():
    return "For moderator"

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', user=user)