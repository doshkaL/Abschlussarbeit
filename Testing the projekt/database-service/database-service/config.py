import os

class Config:
    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'SQLALCHEMY_DATABASE_URI',  # Name der Umgebungsvariable
        'postgresql://postgres:password@postgres:5432/feedback_db'  # Standardwert
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False



