from flask import Flask, request, jsonify
import json
import os
import threading

app = Flask(__name__)

FEEDBACK_FILE = "feedback.json"
API_KEYS = [key.strip() for key in os.environ.get("API_KEYS", "987654321@D").split(",") if key.strip()]

# Lock for synchronizing access to feedback file
feedback_lock = threading.Lock()

def load_feedback():
    feedback = []
    try:
        feedback_lock.acquire()
        if os.path.exists(FEEDBACK_FILE):
            with open(FEEDBACK_FILE, "r") as f:
                feedback = json.load(f)
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
    except IOError as e:
        print(f"IO Error: {e}")
    finally:
        feedback_lock.release()
    return feedback

def save_feedback(feedback):
    try:
        feedback_lock.acquire()
        with open(FEEDBACK_FILE, "w") as f:
            json.dump(feedback, f, indent=4)
    except IOError as e:
        print(f"IO Error while saving feedback: {e}")
    finally:
        feedback_lock.release()

@app.route("/feedback", methods=["POST"])
def receive_feedback():
    api_key = request.headers.get("X-API-Key")
    if not api_key or api_key not in API_KEYS:
        print(f"Unauthorized access attempt with API Key: {api_key}")
        return jsonify({"error": "Invalid API Key"}), 401

    data = request.get_json()
    if not data:
        print("No JSON data provided in the request.")
        return jsonify({"error": "No JSON data provided"}), 400

    if not isinstance(data.get("commit"), str) or not data["commit"]:
        print("Invalid 'commit' field in feedback data.")
        return jsonify({"error": "Commit must be a non-empty string"}), 400

    if not isinstance(data.get("branch"), str) or not data["branch"]:
        print("Invalid 'branch' field in feedback data.")
        return jsonify({"error": "Branch must be a non-empty string"}), 400

    try:
        feedback = load_feedback()
        feedback.append(data)
        save_feedback(feedback)
        print(f"Feedback received: {data}")
        return jsonify({"message": "Feedback successfully received"}), 201
    except Exception as e:
        print(f"Error processing feedback: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug, host='0.0.0.0', port=5000)