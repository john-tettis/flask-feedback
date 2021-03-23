from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ ='users'
    username = db.Column(db.String(20), unique=True,primary_key=True)

    password = db.Column(db.String, nullable=False)

    email = db.Column(db.String(50), nullable=False)

    first_name = db.Column(db.String(30), nullable=False)

    last_name = db.Column(db.String(30), nullable=False)

    @classmethod
    def register(cls, first_name, last_name, email, password, username):
        hash = bcrypt.generate_password_hash(password)
        hash = hash.decode('utf8')

        return cls(first_name=first_name, last_name=last_name, email=email, password = hash, username = username)
    
    @classmethod
    def authenticate(cls, username,password):
        u = User.query.filter(User.username == username).first()

        if u and bcrypt.check_password_hash(u.password, password):
            return u
        else:
            return False
    
    def _full_name(self):
            return f'{self.first_name} {self.last_name}'
    full_name = property(_full_name)


class Feedback(db.Model):
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True, auto_increment=True)

    title = db.Column(db.String(100),nullable = False)

    content = db.Column(db.Text, nullable = False)

    username = db.Column(db.String, db.ForeignKey('users.username'), on_delete = 'cascade')

    user = db.relationship('User', backref = 'feedback')
