from app import db,loginmanager
from datetime import date,time
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@loginmanager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    is_admin=db.Column(db.Boolean())
    is_technician=db.Column(db.Boolean())
    type=db.Column(db.String(55),default='normal')
    phone=db.Column(db.Integer)
    devices=db.relationship('Device',backref='user',lazy='dynamic')


    def __repr__(self):
        return '<User {}>'.format(self.username)

class Device(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(255))
    model=db.Column(db.String(100))
    fault=db.Column(db.String(255))
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    repair_price=db.Column(db.Integer(),default=1)
    status=db.Column(db.String(100),default='booked')

