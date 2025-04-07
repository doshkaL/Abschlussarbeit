
from app import app, db, User
import json
import pytest
from flask import Flask


@pytest.fixture
def client():
    """Test Client für Flask-App mit einer In-Memory-Datenbank."""
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    client = app.test_client()

    with app.app_context():
        db.create_all()
    
    yield client
    
    with app.app_context():
        db.session.remove()
        db.drop_all()

def test_import_data_success(client):
    """Test für erfolgreichen Import von Kursdaten."""
    # Erstelle Instructor und Student in der Test-Datenbank
    with app.app_context():
        instructor = User(username="instructor1", name="Dr. Smith")
        student = User(username="student1", name="Alice")
        db.session.add_all([instructor, student])
        db.session.commit()

    data = [
        {
            "course_id": 1,
            "course_name": "Python Kurs",
            "owner": {"name": "Dr. Smith"},
            "students": [
                {
                    "name": "Alice",
                    "username": "student1",
                    "exercises": [
                        {
                            "id": 101,
                            "exercise_name": "Übung 1",
                            "test_result": "Bestanden",
                            "grade_result": "Erzielte Punkte: 5/10 Note: 2.5",
                            "due_date": "2025-02-07",
                            "submitted_at": "2025-02-07T12:00:00"
                        }
                    ]
                }
            ]
        }
    ]

    response = client.post("/feedback", json=data)
    assert response.status_code == 201
    assert response.json["message"] == "Data imported"

def test_import_data_missing_key(client):
    """Test für fehlende Schlüssel im JSON-Body."""
    data = [
        {
            "course_id": 1,  # Fehlendes 'course_name'
            "owner": {"name": "Dr. Smith"},
            "students": []
        }
    ]

    response = client.post("/feedback", json=data)
    assert response.status_code == 400
    assert "Missing key" in response.json["error"]

def test_import_data_instructor_not_found(client):
    """Test für Instructor, der nicht existiert."""
    data = [
        {
            "course_id": 1,
            "course_name": "Python Kurs",
            "owner": {"name": "Dr. Smith"},  # Instructor existiert nicht
            "students": []
        }
    ]

    response = client.post("/feedback", json=data)
    assert response.status_code == 404
    assert "Instructor Dr. Smith does not exist." in response.json["error"]

def test_import_data_student_not_found(client):
    """Test für Student, der nicht existiert."""
    with app.app_context():
        instructor = User(username="instructor1", name="Dr. Smith")
        db.session.add(instructor)
        db.session.commit()

    data = [
        {
            "course_id": 1,
            "course_name": "Python Kurs",
            "owner": {"name": "Dr. Smith"},
            "students": [
                {
                    "name": "Alice",  # Student existiert nicht
                    "username": "student1",
                    "exercises": []
                }
            ]
        }
    ]

    response = client.post("/feedback", json=data)
    assert response.status_code == 404
    assert "Student Alice does not exist." in response.json["error"]

def test_import_data_empty_request(client):
    """Test für eine leere JSON-Anfrage."""
    response = client.post("/feedback", json=[])
    assert response.status_code == 400
    assert "No data provided" in response.json["error"]
