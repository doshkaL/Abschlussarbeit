from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matrikelnummer = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'student' oder 'instructor'
