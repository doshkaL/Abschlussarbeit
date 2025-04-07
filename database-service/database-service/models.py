from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
from sqlalchemy import CheckConstraint

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    username = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        CheckConstraint("role IN ('student', 'instructor')", name="check_role"),
    )


    
class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    instructor_name = db.Column(db.String(255),  nullable=False)
    instructor_username = db.Column(
        db.String(255),
        db.ForeignKey('user.username'),  
    
        nullable=True
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    course_id = db.Column(
        db.String(255),
        db.ForeignKey('courses.id'),
        nullable=False
    )
    student_name = db.Column(db.String(255))  # Spalte für den Namen des Studenten
    student_username = db.Column(
        db.String(255),
        db.ForeignKey('user.username'),
        nullable=False
    )
    feedback = db.Column(db.Text, nullable=True)
    grade_result = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.Date, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
