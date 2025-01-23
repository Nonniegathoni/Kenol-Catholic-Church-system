from . import db
from flask_login import UserMixin
from sqlalchemy import func

class Uploadannouncement(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    date= db.Column(db.DateTime(timezone=True))
    pdf_data = db.Column(db.LargeBinary)
    filename=db.Column(db.String(150))

def get_pdf_for_date(date):
    return Uploadreading.query.filter_by(date=date).first()

def get_pdf_for_dateannouncement(date):
    return Uploadannouncement.query.filter_by(date=date).first()

class Uploadreading(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    date= db.Column(db.DateTime(timezone=True))
    pdf_data = db.Column(db.LargeBinary)
    filename=db.Column(db.String(150))

class Audio(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    audio_data = db.Column(db.LargeBinary)
    name=db.Column(db.String(255))


    
class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    first_name=db.Column(db.String(150))
    last_name=db.Column(db.String(150))
    group=db.Column(db.String(150))
    small_christian_community=db.Column(db.String(150))
    password=db.Column(db.String(150))
    phone=db.Column(db.String(100))

class Admin(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    first_name=db.Column(db.String(150))
    last_name=db.Column(db.String(150))
    designation=db.Column(db.String(150))
    email=db.Column(db.String(150), unique=True)
    password=db.Column(db.String(150))
    phone=db.Column(db.String(100))

class Baptismbooking(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    candidate_f_name=db.Column(db.String(150))
    candidate_l_name=db.Column(db.String(150))
    candidate_age=db.Column(db.String(50))
    date= db.Column(db.DateTime(timezone=True))
    guardian_f_name=db.Column(db.String(150))
    guardian_l_name=db.Column(db.String(150))
    guardian_phone=db.Column(db.String(50))
    father_f_name=db.Column(db.String(150))
    father_l_name=db.Column(db.String(150))
    father_phone=db.Column(db.String(50))
    mother_f_name=db.Column(db.String(150))
    mother_l_name=db.Column(db.String(150))
    mother_phone=db.Column(db.String(50))

class Confirmationbooking(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    candidate_f_name=db.Column(db.String(150))
    candidate_l_name=db.Column(db.String(150))
    candidate_age=db.Column(db.String(50))
    date= db.Column(db.DateTime(timezone=True))
    guardian_f_name=db.Column(db.String(150))
    guardian_l_name=db.Column(db.String(150))
    guardian_phone=db.Column(db.String(50))
    father_f_name=db.Column(db.String(150))
    father_l_name=db.Column(db.String(150))
    father_phone=db.Column(db.String(50))
    mother_f_name=db.Column(db.String(150))
    mother_l_name=db.Column(db.String(150))
    mother_phone=db.Column(db.String(50))


class Massbooking(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    f_name=db.Column(db.String(150))
    l_name=db.Column(db.String(150))
    scc=db.Column(db.String(150))
    phone=db.Column(db.String(50))
    date=db.Column(db.DateTime(timezone=True))



