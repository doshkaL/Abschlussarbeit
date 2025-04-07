import pytest
import requests
import requests_mock
import bcrypt
from flask import Flask, jsonify
from login_service import app

DATABASE_SERVICE_URL = "http://172.18.0.4:5001/get_user"

@pytest.fixture
def client():
    """Erstellt einen Test-Client für die Flask-App."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def hash_password(password):
    """Hilfsfunktion zum Hashen eines Passworts."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def test_successful_login(client, requests_mock):
    """Testet einen erfolgreichen Login."""
    username = "testuser"
    password = "securepassword"
    hashed_password = hash_password(password)

    requests_mock.post(DATABASE_SERVICE_URL, json={
        "username": username,
        "password_hash": hashed_password,
        "role": "student"
    }, status_code=200)

    response = client.post('/login', json={"username": username, "password": password})
    
    assert response.status_code == 200
    assert response.json["message"] == "Login successful"
    assert response.json["role"] == "student"
    assert response.json["username"] == username

def test_login_user_not_found(client, requests_mock):
    """Testet den Fall, dass der Benutzer nicht existiert."""
    requests_mock.post(DATABASE_SERVICE_URL, status_code=404)

    response = client.post('/login', json={"username": "unknown", "password": "test"})
    
    assert response.status_code == 404
    assert response.json["error"] == "Invalid username or password"

def test_login_invalid_password(client, requests_mock):
    """Testet den Fall, dass das Passwort falsch ist."""
    username = "testuser"
    hashed_password = hash_password("correct_password")

    requests_mock.post(DATABASE_SERVICE_URL, json={
        "username": username,
        "password_hash": hashed_password,
        "role": "student"
    }, status_code=200)

    response = client.post('/login', json={"username": username, "password": "wrongpassword"})
    
    assert response.status_code == 401
    assert response.json["error"] == "Invalid username or password"

def test_login_missing_username(client):
    """Testet den Fall, dass kein Benutzername angegeben wurde."""
    response = client.post('/login', json={"password": "testpassword"})
    
    assert response.status_code == 400
    assert response.json["error"] == "Username and password are required"

def test_login_missing_password(client):
    """Testet den Fall, dass kein Passwort angegeben wurde."""
    response = client.post('/login', json={"username": "testuser"})
    
    assert response.status_code == 400
    assert response.json["error"] == "Username and password are required"

def test_database_service_error(client, requests_mock):
    """Testet den Fall, dass der Database-Service einen Fehler zurückgibt."""
    requests_mock.post(DATABASE_SERVICE_URL, status_code=500)

    response = client.post('/login', json={"username": "testuser", "password": "testpassword"})
    
    assert response.status_code == 401
    assert response.json["error"] == "Invalid username or password"

