from flask_sqlalchemy import SQLAlchemy
import bcrypt

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        salt = bcrypt.gensalt(rounds=12)
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

class CommonPassword(db.Model):
    __tablename__ = 'common_passwords'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(256), unique=True, nullable=False)

    @staticmethod
    def is_common(password):
        return db.session.query(CommonPassword).filter_by(
            password=password.lower().strip()
        ).first() is not None