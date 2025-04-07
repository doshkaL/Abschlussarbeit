import requests
import bcrypt
from flask import Flask, request, jsonify

app = Flask(__name__)

DATABASE_SERVICE_URL = "http://172.18.0.3:5001/get_user"

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    print(f"Login-Anfrage erhalten für Benutzer: {username}")

    # Anfrage an den Database-Service
    response = requests.post(DATABASE_SERVICE_URL, json={'username': username})

    if response.status_code == 404:
        return jsonify({'error': 'User not found'}), 404

    if response.status_code != 200:
        return jsonify({'error': 'Invalid username or password'}), 401  # Korrigiert auf 401 Unauthorized

    user_data = response.json()
    stored_hashed_password = user_data.get('password_hash')

    #  Passwort mit bcrypt prüfen
    if not stored_hashed_password or not bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
        print(" Passwortprüfung fehlgeschlagen")
        return jsonify({'error': 'Invalid username or password'}), 401

    print(f"✅ Login erfolgreich für {username}")

    return jsonify({
        "message": "Login successful",
        "role": user_data["role"],
        "username": username  # Füge den Benutzernamen zur Antwort hinzu!
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
