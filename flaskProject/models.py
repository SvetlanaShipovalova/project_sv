from app import db

class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), unique = True)
    users = db.relationship("User", backref = "role")

    def __repr__(self):
        return "<Role %r>" % self.name

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(60), unique = True, index = True)
    password = db.Column(db.String(60))
    email = db.Column(db.String(60))
    gender = db.Column(db.String(60))
    role_id = db.Column(db.Integer,  db.ForeignKey("roles.id"))

    def __repr__(self):
        return "<User %r>" % self.username

