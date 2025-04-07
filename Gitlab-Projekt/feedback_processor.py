import os
import json
import requests
from datetime import datetime
import sys

def get_project_owner(api_url, project_id, access_token):
    """
    Fetches the project owner from the GitLab API.
    """
    headers = {"Private-Token": access_token}
    url = f"{api_url}/projects/{project_id}"

    try:
        response = requests.get(url, headers=headers)
        
        # Handle specific HTTP error codes separately
        if response.status_code == 404:
            print("Error: Project not found.")
            return "unknown_owner"
        elif response.status_code == 403:
            print("Error: Access forbidden. Check your API token.")
            return "unknown_owner"
        elif response.status_code >= 500:
            print("Error: GitLab server issue. Try again later.")
            return "unknown_owner"
        
        response.raise_for_status()
        project_data = response.json()
        namespace = project_data.get("namespace", {})
        
        # Check if the project is under a group or individual user
        if namespace.get("kind") == "group":
            return f"Group: {namespace.get('name', 'unknown_group')}"
        return namespace.get("name", "unknown_owner")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching project owner: {e}")
        return "unknown_owner"

def read_file_content(file_path):
    """
    Reads the content of a file and returns it as a string.
    """
    try:
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                return file.read().strip()
        print(f"File '{file_path}' is missing or empty.")
        return ""
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return ""

def create_feedback_json(project_id, project_name, owner_name, user_name, user_username, commit_timestamp, exercises_data):
    """
    Creates a JSON structure for feedback data and writes it to a file.
    """
    feedback_data = [
        {
            "course_id": project_id,
            "course_name": project_name,
            "owner": {"name": owner_name},
            "students": [
                {
                    "username": user_username,
                    "name": user_name,
                    "exercises": exercises_data
                }
            ]
        }
    ]

    with open("feedback.json", "w") as file:
        json.dump(feedback_data, file, indent=4)
    print("Feedback JSON created as 'feedback.json'.")

    return feedback_data

if __name__ == "__main__":
    # Retrieve environment variables and command-line arguments
    FEEDBACK_DIR = sys.argv[1]
    API_URL = os.getenv("GITLAB_API_URL", "http://localhost/api/v4")
    PROJECT_ID = os.getenv("CI_PROJECT_ID")
    PROJECT_NAME = os.getenv("CI_PROJECT_NAME", "unknown_project_name")
    ACCESS_TOKEN = os.getenv("GITLAB_ACCESS_TOKEN")
    GITLAB_USER_NAME = os.getenv("GITLAB_USER_NAME", "John Doe")
    GITLAB_USER_LOGIN = os.getenv("GITLAB_USER_LOGIN", "johndoe")
    COMMIT_TIMESTAMP = os.getenv("CI_COMMIT_TIMESTAMP", datetime.now().isoformat())

    # Validate environment variables
    if not PROJECT_ID or not ACCESS_TOKEN:
        print("Missing PROJECT_ID or ACCESS_TOKEN. Check environment variables.")
        exit(1)

    exercises_data = []

    # Process feedback directory and extract results
    for file in os.listdir(FEEDBACK_DIR):
        if file.endswith("-lint-result.txt"):
            exercise_name = file.replace("-lint-result.txt", "")
            lint_results = read_file_content(os.path.join(FEEDBACK_DIR, file))
            autograde_results = read_file_content(os.path.join(FEEDBACK_DIR, f"{exercise_name}-autograde-result.txt"))
            
            # Ensure both lint and autograde results exist before adding to exercises
            if lint_results and autograde_results:
                exercises_data.append({
                    "id": f"001-{exercise_name}",
                    "exercise_name": exercise_name,
                    "test_result": lint_results,
                    "grade_result": autograde_results,
                    "due_date": "2024-06-10",
                    "submitted_at": COMMIT_TIMESTAMP
                })
            else:
                print(f"Missing results for {exercise_name}. Skipping...")

    # Fetch project owner information
    owner_name = get_project_owner(API_URL, PROJECT_ID, ACCESS_TOKEN)

    # Generate feedback JSON only if valid exercises exist
    if exercises_data:
        feedback_data = create_feedback_json(
            project_id=PROJECT_ID,
            project_name=PROJECT_NAME,
            owner_name=owner_name,
            user_name=GITLAB_USER_NAME,
            user_username=GITLAB_USER_LOGIN,
            commit_timestamp=COMMIT_TIMESTAMP,
            exercises_data=exercises_data
        )
        # Print JSON to console for debugging or simulation purposes
        print(json.dumps(feedback_data, indent=4))
    else:
        print("No valid exercises found. No feedback created.")
