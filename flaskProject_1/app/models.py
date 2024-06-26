from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from authlib.jose import JsonWebSignature
from flask_login import UserMixin, AnonymousUserMixin


class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Moderator': [Permission.FOLLOW, Permission.COMMENT,
                          Permission.WRITE, Permission.MODERATE],
            'Administrator': [Permission.FOLLOW, Permission.COMMENT,
                              Permission.WRITE, Permission.MODERATE,
                              Permission.ADMIN],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(60), unique=True, index=True)
    descript = db.Column(db.String(300))
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, default=False)
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.id'))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == "testosvet@gmail.com":
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_admin(self):
        return self.can(Permission.ADMIN)

    def is_driver(self):
        return self.can(Permission.MODERATE)

    class AnonymousUser(AnonymousUserMixin):
        def can(self, perm):
            return False

        def is_admin(self):
            return False

    login_manager.anonymous_user = AnonymousUser

    def generate_confirmation_token(self):
        jws = JsonWebSignature()
        protected = {'alg': 'HS256'}
        payload = self.id
        secret = 'secret'
        return jws.serialize_compact(protected, payload, secret).decode('utf-8')

    def confirm(self, token):
        jws = JsonWebSignature()
        data = jws.deserialize_compact(s=token, key='secret')
        if data.payload.decode('utf-8') != str(self.id):
            print("It's not you token")
            return False
        else:
            self.confirmed = True
            db.session.add(self)
            return True

    @property
    def password(self):
        raise AttributeError('password not enable for read')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def password_verify(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Bus(db.Model):
    __tablename__ = 'buses'
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(60), index=True, unique=True)
    number = db.Column(db.String(60), index=True)
    route = db.Column(db.String(300))
    schedule = db.Column(db.String(300))
    img = db.Column(db.String(300))
    condition = db.Column(db.String(300))
    working_shift = db.Column(db.Boolean, default=False)
    users = db.relationship('User', backref='bus', lazy='dynamic')

    def __repr__(self):
        return '<Bus %r>' % self.model


class Mark(db.Model):
    __tablename__ = 'marks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.id'))
    selected = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Mark %r>' % self.id
