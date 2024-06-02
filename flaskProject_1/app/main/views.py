from flask import render_template, redirect, url_for, session, abort
from flask_admin.contrib.sqla import ModelView
from app.models import User, Permission, Role, Bus, Mark
from . import main
from ..decorators import admin_required, permission_required
from flask_login import login_required, current_user
from .. import db, admin


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


@main.route("/secret")
@login_required
def secret():
    print("test login")
    return "Only for auth"


@main.route("/testConfirm")
def test_confirm():
    user = User.query.filter_by().first()
    tmp = user.generate_confirmation_token()
    user.confirm(tmp)


@main.route('/admin/')
@login_required
@admin_required
def for_admin():
    return render_template('admin.html', user=user)


class MyModelView(ModelView):
    def is_accessible(self):
        """
        Регулирует доступность видимости пользователям админ-панели.
        Вне функции создается представление модели пользователей, ролей и автобусов.
        В классе MyModelView мы переопределяем работу ModelView с использованием библиотеки Flask-Admin.
        Функция is_accessible проверяет, является ли текущий пользователь администратором
        и, если да, перенаправляет его на главную страницу административной панели.
        Эти объекты MyModelView добавляются в flask-admin из db.
        """
        if User.is_admin(current_user):
            return redirect(url_for('main.admin'))


admin.add_view(MyModelView(User, db.session, name="Пользователи"))
admin.add_view(MyModelView(Role, db.session, name="Роли"))
admin.add_view(MyModelView(Bus, db.session, name="Автобусы"))


@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def for_moderator():
    """
    Страница, отображаемая для пользователей с ролью "Водитель".
    Пользователь видит информацию об закрепленном за ним автобусе, может открывать/закрывать рабочую смену.
    Отдельно, на этой же странице, он может просматривать других водителей, находящихся сейчас на рабочей смене.
    """
    user = User.query.filter_by(bus_id=Bus.id).all()
    bus = Bus.query.filter_by(id=User.bus_id).all()
    other_bus = Bus.query.filter(Bus.id != User.bus_id).filter_by(working_shift=True).all()
    return render_template('for_users.html', user=user, bus=bus, other_bus=other_bus)


@main.route('/check_work')
@login_required
@permission_required(Permission.MODERATE)
def check_work():
    """
    Функция, отвечающая за открытые/закрытие смены.
    Фильтрует автобусы по принадлежности пользователю, проверяет данные с db и обновляет их.
    """
    if Bus.query.filter_by(id=User.bus_id).filter_by(working_shift=True).first():
        Bus.query.filter_by(id=User.bus_id).update(dict(working_shift=0))
    else:
        Bus.query.filter_by(id=User.bus_id).update(dict(working_shift=1))
    db.session.commit()
    return redirect(url_for('main.for_moderator'))


@main.route('/user/<username>')
def user(username):
    """
    Страница, отображаемая для обычных пользователей с ролью "User", либо None.
    Выводит таблицу, содержащую сведения об автобусах, находящихся на маршруте в данный момент, расписание и их направление.
    """
    bus = Bus.query.filter_by(working_shift=True).all()
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('for_users.html', user=user, bus=bus)


@main.route('/marks/<username>')
def marks(username):
    """
    Страница с отмеченными как избранное автобусами, для более быстрого поиска конкретного.
    """
    bus = []
    user = User.query.filter_by(username=username).first_or_404()
    if (Mark.query.filter_by(user_id=user.id).all()):
        bus = Bus.query.filter_by(id=Mark.bus_id).all()
    return render_template('marks.html', bus=bus)


@main.route("/add_mark/<username>/<bus_id>", methods=['GET', 'POST'])
def add_mark(username, bus_id):
    """
    Добавление отметки "Избранное".
    Функция получает параметры пользователя и отмеченного им автобуса и создает объект модели.
    После происходит перенаправление на главную страницу с информацией о пользователе.
    """
    bus = Bus.query.filter_by(id=bus_id).first_or_404()
    user = User.query.filter_by(username=username).first_or_404()
    mark = Mark(user_id=user.id,
                bus_id=bus.id,
                selected=True)
    db.session.add(mark)
    db.session.commit()
    return redirect((url_for('main.index')))


@main.route("/remove_mark/<username>/<bus_id>", methods=['GET', 'POST'])
def remove_mark(username, bus_id):
    """
    Удаление отметки "Избранное".
    """
    bus = Bus.query.filter_by(id=bus_id).first_or_404()
    user = User.query.filter_by(username=username).first_or_404()
    mark = Mark.query.filter_by(bus_id=bus.id).filter_by(user_id=user.id).first()
    db.session.delete(mark)
    db.session.commit()
    return redirect((url_for('main.index')))
