import pytest
import json
import sys
import os
from datetime import datetime

# Stelle sicher, dass das Verzeichnis im Python-Pfad ist
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Zuerst die TestConfig importieren, damit sie vor `app` geladen wird
from test_config import TestConfig

# Jetzt die App-Instanz importieren
from app import app, db, User, Course, Exercise



@pytest.fixture(scope="session")
def test_app():
    """Setup Flask test app with SQLite."""
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # Nutzt eine In-Memory SQLite DB

    with app.app_context():
        db.create_all()  # Erstellt Tabellen für Tests

    yield app  # Die App wird für Tests bereitgestellt

    with app.app_context():
        db.session.remove()
        db.drop_all()  # Bereinigt die DB nach Tests


@pytest.fixture
def client(test_app):
    """Erstelle einen Test-Client für Requests."""
    with test_app.app_context():
        return test_app.test_client()

@pytest.fixture(autouse=True)
def clean_db():
    """Löscht die Datenbank nach jedem Test"""
    yield
    with app.app_context():
        db.session.rollback()
        db.drop_all()
        db.create_all()

def test_import_data_success(client):
    """Test für erfolgreichen Import von Kursdaten."""
    with app.app_context():
        instructor = User(username="instructor1", name="Dr. Smith",password="1234",role="instructor")
        student = User(username="student1", name="Alice",password="1234",role="student")
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
    print(response.json)  # Debugging: Die echte API-Antwort ausgeben
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
    print(response.json)  # Debugging
    assert response.status_code == 404  
    assert "Instructor Dr. Smith does not exist." in response.json["error"]



def test_import_data_student_not_found(client):
    """Test für Student, der nicht existiert."""
    with app.app_context():
     existing_instructor = User.query.filter_by(username="instructor1").first()
     if not existing_instructor:
        instructor = User(username="instructor1", name="Dr. Smith", password="test123", role="instructor")
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
    print(response.json)
    assert response.status_code == 404
    assert "Student Alice does not exist." in response.json["error"]




def test_get_instructor_courses_success(client):
    """Testet, ob der Instructor erfolgreich seine Kurse abrufen kann."""
    with app.app_context():
        #  Instructor & Student anlegen
        instructor = User(username="s064450330", name="Dr. Smith", password="test123", role="instructor")
        student = User(username="student1", name="Alice", password="test123", role="student")
        db.session.add_all([instructor, student])
        db.session.commit()  #  WICHTIG: Daten speichern!

        #  Kurs anlegen
        course = Course(id=1, name="Python Kurs", instructor_name="Dr. Smith", instructor_username="s064450330")
        db.session.add(course)
        db.session.commit()  # Kurs speichern

        # Übung für den Kurs anlegen (Fix: `date()` für `due_date`)
        exercise = Exercise(
            id=101,
            name="Übung 1",
            course_id=1,
            student_name="Alice",
            student_username="student1",
            feedback="Bestanden",
            grade_result="Erzielte Punkte: 5/10 Note: 2.5",
            due_date=datetime.strptime("2025-02-07", "%Y-%m-%d").date(),  #  SQLite benötigt `date`
            submitted_at=datetime.strptime("2025-02-07T12:00:00", "%Y-%m-%dT%H:%M:%S"),  #  SQLite benötigt `datetime`
        )
        db.session.add(exercise)
        db.session.commit()  #  Übung speichern

    instructor_username = "s064450330"

    # Anfrage an den Endpunkt senden
    response = client.get(f"/instructor/courses?username={instructor_username}")  
    print("DEBUG API Response:", response.get_json())  #  Debug-Ausgabe

    # Fehleranalyse: Falls `500`, die Fehlermeldung ausgeben
    if response.status_code == 500:
        print(" ERROR:", response.get_json())

    assert response.status_code == 200  #  API sollte 200 zurückgeben
    data = response.get_json()

    #  Sicherstellen, dass mindestens ein Kurs existiert
    assert len(data) > 0, " Die API gibt keine Kurse zurück!"
    assert int(data[0]["id"]) == 1  
    assert data[0]["name"] == "Python Kurs"
    assert len(data[0]["students"]) > 0  # Mindestens ein Student
    assert data[0]["students"][0]["name"] == "Alice"
      #  Falls `due_date` ein String ist, `.isoformat()` nicht aufrufen
    assert data[0]["students"][0]["exercises"][0]["due_date"] == "2025-02-07"



def test_get_student_courses_success(client):
    """Testet, ob ein Student erfolgreich seine Kurse abrufen kann."""
    with app.app_context():
        # Instructor und Student anlegen
        instructor = User(username="instructor1", name="Dr. Smith", password="test123", role="instructor")
        student = User(username="student1", name="Alice", password="test123", role="student")
        db.session.add_all([instructor, student])
        db.session.commit()

        # Kurs anlegen
        course = Course(id=1, name="Python Kurs", instructor_name="Dr. Smith", instructor_username="instructor1")
        db.session.add(course)
        db.session.commit()

        # Übung für den Kurs anlegen
        exercise = Exercise(
            id=101,
            name="Übung 1",
            course_id=1,
            student_name="Alice",
            student_username="student1",
            feedback="Bestanden",
            grade_result="Erzielte Punkte: 5/10 Note: 2.5",
          due_date=datetime.strptime("2025-02-07", "%Y-%m-%d").date(),  # **Fix**
          submitted_at=datetime.strptime("2025-02-07T12:00:00", "%Y-%m-%dT%H:%M:%S"),
        )
        db.session.add(exercise)
        db.session.commit()

    # Anfrage an den Endpunkt senden
    response = client.get("/student/courses?username=student1")
    assert response.status_code == 200
    data = response.get_json()

    # Überprüfen, ob der Kurs korrekt zurückgegeben wurde
    assert len(data) > 0  # Es sollte Kurse geben
    assert int(data[0]["course_id"]) == 1  
    assert data[0]["course_name"] == "Python Kurs"
    assert len(data[0]["students"]) > 0  # Mindestens ein Student
    assert data[0]["students"][0]["id"] == "student1"
    assert data[0]["students"][0]["name"] == "Alice"
    assert int(data[0]["students"][0]["exercises"][0]["id"]) == 101  # **Fix für ID**






