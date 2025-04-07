#from app import db
#from flask_sqlalchemy import SQLAlchemy
#from datetime import datetime
##import uuid
#from sqlalchemy import CheckConstraint

#c#lass User(db.Model):
  #  __tablename__ = 'user'

   # username = db.Column(db.String(255), primary_key=True)
  #  name = db.Column(db.String(255), nullable=False)
  #  password = db.Column(db.String(255), nullable=False)
  #  role = db.Column(db.String(50), nullable=False)
   # created_at = db.Column(db.DateTime, default=datetime.utcnow)
 #   updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

   # __table_args__ = (
   #     CheckConstraint("role IN ('student', 'instructor')", name="check_role"),
   # )
