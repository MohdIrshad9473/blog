from main import db

class Registation(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    First_Name = db.Column(db.String(80), nullable=False)
    Last_Name = db.Column(db.String(80), nullable=False)
    Dob = db.Column(db.DateTime, nullable=False)
    Email = db.Column(db.String(100), nullable=False, unique=True)
    Password = db.Column(db.String(300), nullable=False)
    otp = db.Column(db.Integer, nullable=False)