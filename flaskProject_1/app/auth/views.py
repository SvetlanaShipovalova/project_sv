from flask import render_template, redirect, request, flash, url_for
from flask_mail import Message
from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import User
from flask_login import login_user, login_required, logout_user, current_user
from threading import Thread
from app import mail


@auth.before_app_request
def before_request():
    """
    @auth.before_app_request` - декоратор, который сообщает Flask запускать функцию `before_request`
    перед каждым запросом к приложению. Происходит проверка условий перед авторизацией пользователя.
    """
    if current_user.is_authenticated and not current_user.confirmed and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Функция создает экземпляр формы LoginForm().
    Если форма была отправлена и прошла валидацию, то ищет пользователя в базе данных по электронной почте из формы.
    Проверяет, что пользователь существует и его пароль соответствует введенному в форме.
    Если пользователь прошел аутентификацию, выполняет вход пользователя.
    Проверяет параметр "next" из запроса, чтобы определить, куда перенаправить пользователя после входа.
    Если вход не был выполнен успешно, выводит сообщение об ошибке на экран.
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.password_verify(form.password.data):
            login_user(user)
            next = request.args.get("next")
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Ivalid username or password')
    return render_template("auth/login.html", form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
     Функция создает форму регистрации и проверяет, была ли форма заполнена и отправлена корректно.
     Если это так, то создается новый пользователь с данными из формы, добавляется в базу данных, устанавливается пароль,
     и данные коммитятся в базу данных.
     Затем генерируется токен подтверждения и отправляется пользователю для подтверждения его регистрации.
     После этого происходит перенаправление на страницу входа.
     Если форма не была правильно заполнена или отправлена, то происходит рендеринг шаблона регистрации с указанием этой формы.
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    descript=form.description.data)
        db.session.add(user)
        user.set_password(form.password.data)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_confirm(user, token)
        return redirect(url_for('auth.login'))
    return render_template("auth/registration.html", form=form)


@auth.route('/logout')
@login_required
def logout():
    """
    Функция отвечает за прекращение сеанса работы пользователя и возвращает нас на главную страницу.
    """
    logout_user()
    flash("You are logout")
    return redirect((url_for('main.index')))


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    """
    Эта функция принимает токен в качестве аргумента и проверяет его наличие.
    Если пользователь уже подтвержден, то происходит перенаправление на главную страницу сайта.
    Если пользователь еще не подтвержден, то вызывается метод с переданным токеном.
    Если подтверждение прошло успешно, то происходит коммит к базе данных,
    выводится сообщение о успешном подтверждении и происходит перенаправление на главную страницу сайта.
    Если метод confirm() возвращает False, то выводится сообщение о невалидной или истекшей ссылке
    и происходит перенаправление на главную страницу сайта.
    """
    print(token)
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash("Ваше подтверждение прошло успешно, спасибо!")
    else:
        flash("Ваша ссылка не валидна или истекла")
    return redirect(url_for('main.index'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


def send_confirm(user, token):
    send_mail(user.email, 'Confirm your account', 'auth/confirm', user=user, token=token)
    redirect(url_for('main.index'))


def send_mail(to, subject, template, **kwargs):
    """
    В функции создается объект сообщения (msg) с указанием отправителя и получателя.
    Затем происходит попытка отрендерить текст сообщения с помощью шаблона HTML.
    Если это не удалось, то текст рендерится с помощью шаблона TXT.
    После этого из файла app_file импортируется объект flask_app, который используется для создания многопоточности.
    Создается отдельный поток (thread) с целью выполнить функцию send_async_email асинхронно (без блокирования основного потока).
    После запуска потока, функция возвращает объект потока.
    """
    msg = Message(subject,
                  sender="testosvet@gmail.com",
                  recipients=[to])
    try:
        msg.html = render_template(template + ".html", **kwargs)
    except:
        msg.body = render_template(template + ".txt", **kwargs)
    from app_file import flask_app
    thread = Thread(target=send_async_email, args=[flask_app, msg])
    thread.start()
    return thread


def send_async_email(app, msg):
    """
    Функция send_async_email принимает объект и сообщение.
    С помощью менеджера контекста приложения, используется mail.send для отправки сообщения.
    """
    with app.app_context():
        mail.send(msg)
