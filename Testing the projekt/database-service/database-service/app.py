from flask import Flask, request, jsonify
from sqlalchemy import text
from config import Config
from models import db, User, Course, Exercise
from mappers import user_dto_to_model
from dto_models import UserDTO
from pydantic import ValidationError
import logging
from datetime import date, datetime
from dateutil.parser import parse
from sqlalchemy import exc 
import re

# Initialize Flask app
app = Flask(__name__)
##app.config.from_object(Config)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
app.config["TESTING"] = True

# Initialize SQLAlchemy
db.init_app(app)
    
# Initialize database tables
with app.app_context():
    db.create_all()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Extrahiere die Punktzahl, Note und detaillierte Gradegebnisse aus dem grade_result
def extract_grade_details(grade_result):
    # Extrahiere die Punktzahl und Note
    grade_details_match = re.search(r"Erzielte Punkte: (\d+/\d+)\s*Note: (\d+\.\d)", grade_result)
    if grade_details_match:
        points = grade_details_match.group(1)
        grade = grade_details_match.group(2)
        grade_details = f"Erzielte Punkte: {points}\nNote: {grade}"
    else:
        grade_details = "Keine Noteninformationen gefunden"
    
    # Extrahiere die detaillierten Gradegebnisse
    test_details_matches = re.findall(r"(\S+): (Bestanden|Nicht bestanden), Punkte: (\d+)/(\d+)", grade_result)
    test_details = ""
    for test_name, status, obtained_points, max_points in test_details_matches:
        test_details += f"{test_name}: {status}, Punkte: {obtained_points}/{max_points}\n"
    
    if not test_details:
        test_details = "Keine Testergebnisse gefunden"
    
    # Kombiniere die Ergebnisse
    full_grade_result = f"{grade_details}\n\nDetaillierte Ergebnisse:\n{test_details}"
    
    return full_grade_result




@app.route('/feedback', methods=['POST'])
def import_data():
    try:
        data = request.get_json()
        logging.info(f"Received data: {data}")

        if not data:  # Check if data is empty or None
            logging.error("No data received in request.")
            return jsonify({"error": "No data provided"}), 400

        db.session.begin()

        for record in data:
            required_keys = ["course_id", "course_name", "owner", "students"]
            for key in required_keys:
                if key not in record:
                    logging.error(f"Missing key: {key}")
                    db.session.rollback()
                    return jsonify({"error": f"Missing key: {key}"}), 400

            instructor_data = record['owner']
            instructor = User.query.filter_by(name=instructor_data['name']).first()
            if not instructor:
                logging.error(f"Instructor {instructor_data['name']} not found.")
                db.session.rollback()
                return jsonify({"error": f"Instructor {instructor_data['name']} does not exist."}), 404

            instructor_username = instructor.username

            course = Course.query.filter_by(id=record['course_id']).first()
            if not course:
                course = Course(
                    id=record['course_id'],
                    name=record['course_name'],
                    instructor_name=instructor.name,
                    instructor_username=instructor_username,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.session.add(course)
            else:
                course.name = record['course_name']
                course.instructor_username = instructor_username
                course.updated_at = datetime.utcnow()

            student_names = [s['name'] for s in record['students']]
            students = {s.name: s for s in User.query.filter(User.name.in_(student_names)).all()}

            if not record['students']:  # Check for empty student list
                logging.warning(f"No students found for course {record['course_id']}")
                continue # Skip to the next record

            for student in record['students']:
                student_entry = students.get(student['name'])
                if not student_entry:
                    logging.error(f"Student {student['name']} not found.")
                    db.session.rollback()
                    return jsonify({"error": f"Student {student['name']} does not exist."}), 404

                if not student['exercises']: # Check for empty exercises list
                    logging.warning(f"No exercises found for student {student['name']}")
                    continue # Skip to the next student

                for exercise in student['exercises']:
                    extracted_grade = extract_grade_details(exercise['grade_result'])

                    exercise_entry = Exercise.query.filter_by(id=exercise['id'], course_id=record['course_id'], student_name=student['name']).first()
                    if not exercise_entry:
                        exercise_entry = Exercise(
                            id=exercise['id'],
                            name=exercise['exercise_name'],
                            course_id=record['course_id'],
                            student_name=student['name'],
                            student_username=student['username'],
                            feedback=exercise['test_result'],
                            grade_result=extracted_grade,
                            due_date=datetime.strptime(exercise['due_date'], '%Y-%m-%d'),
                            submitted_at=parse(exercise['submitted_at'])
                        )
                        db.session.add(exercise_entry)
                    else:
                        exercise_entry.name = exercise['exercise_name']
                        exercise_entry.feedback = exercise['test_result']
                        exercise_entry.grade_result = extracted_grade
                        exercise_entry.due_date = datetime.strptime(exercise['due_date'], '%Y-%m-%d')
                        exercise_entry.submitted_at = parse(exercise['submitted_at'])

        db.session.commit()
        logging.info("Data successfully saved.")
        return jsonify({"message": "Data imported"}), 201

    except KeyError as e:  # More specific exceptions
        logging.error(f"Missing key: {e}")
        db.session.rollback()
        return jsonify({"error": f"Missing key: {e}"}), 400
    except ValueError as e:
        logging.error(f"Value error: {e}")
        db.session.rollback()
        return jsonify({"error": f"Invalid data: {e}"}), 400
    except exc.IntegrityError as e:  # SQLAlchemy IntegrityError
        logging.error(f"Database integrity error: {e}")
        db.session.rollback()
        return jsonify({"error": "Database integrity error (likely duplicate data)"}), 400
    except Exception as e:  # General exception (last resort)
        logging.error(f"An unexpected error occurred: {e}")
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred"}), 500



    
@app.route('/user', methods=['POST'])
def receive_user():
    try:
        data = request.get_json()
        user_dto = UserDTO(**data)
        logging.info(f"Received user: {user_dto.json()}")

        # Map DTO to model
        user = user_dto_to_model(user_dto)

        # Save to database
        db.session.add(user)
        db.session.commit()
        logging.info(f"User saved with ID: {user.username}")

        return jsonify({'message': 'User received successfully'}), 201

    except ValidationError as e:
        logging.error(f"Validation error: {e}")
        return jsonify({'error': e.errors()}), 400

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@app.route('/instructor/courses', methods=['GET'])
def get_instructor_courses():
    try:
        # Define the SQL query
        sql = text("""
            SELECT 
                c.id AS course_id,
                c.name AS course_name,
                u.username AS student_username,
                u.name AS student_name,
                e.id AS exercise_id,
                e.name AS exercise_name,
                e.feedback AS exercise_feedback,
                e.grade_result AS exercise_grade,
                e.due_date AS exercise_due_date,
                e.submitted_at AS exercise_submitted_at
            FROM 
                courses c
            JOIN 
                exercises e ON c.id = e.course_id
            JOIN 
                "user" u ON e.student_username = u.username
            WHERE 
                 c.instructor_username = :instructor_username
            ORDER BY 
                c.id, u.username;
        """)

        # Execute the query with the instructor's username
        instructor_username = "s064450330"  # Replace with the actual instructor's username
        result = db.session.execute(sql, {"instructor_username": instructor_username})
        
        # Organize the data into the required structure
        courses = {}
        for row in result:
            course_id = row.course_id
            if course_id not in courses:
                courses[course_id] = {
                    "id": row.course_id,
                    "name": row.course_name,
                    "students": []
                }
            due_date = row.exercise_due_date
            submitted_at = row.exercise_submitted_at
            if isinstance(due_date, (datetime, date)):
                due_date = due_date.isoformat()
            if isinstance(submitted_at, datetime):
                submitted_at = submitted_at.isoformat()    
            # Check if the student is already added to the course
            student_exists = False
            for student in courses[course_id]["students"]:
                if student["username"] == row.student_username:
                    student_exists = True
                    # Add the exercise to the student's list
                    student["exercises"].append({
                        "id": row.exercise_id,
                        "name": row.exercise_name,
                        "feedback": row.exercise_feedback,
                        "grade_result": row.exercise_grade,
                        "due_date": due_date,
                        "submitted_at":submitted_at
                    })
                    break

            # If the student is not already added, add them to the course
            if not student_exists:
                courses[course_id]["students"].append({
                    "username": row.student_username,
                    "name": row.student_name,
                    "exercises": [
                        {
                            "id": row.exercise_id,
                            "name": row.exercise_name,
                            "feedback": row.exercise_feedback,
                            "grade_result": row.exercise_grade,
                            "due_date": due_date ,
                            "submitted_at": submitted_at 
                        }
                    ]
                })

        # Convert the dictionary to a list
        course_list = list(courses.values())

        # Return the result as JSON
        return jsonify(course_list), 200

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/student/courses', methods=['GET'])
def get_courses():
    username = request.args.get('username')  # Get the student's username from the query parameters
    if not username:
        return jsonify({'error': 'Username is required'}), 400

    try:
        # Fetch courses where the student has exercises
        courses = db.session.query(Course).join(Exercise).filter(Exercise.student_username == username).distinct().all()

        # Format the response
        courses_data = []
        for course in courses:
            # Fetch the course owner (instructor)
            instructor = User.query.filter_by(username=course.instructor_username).first()
            if not instructor:
                continue

            # Fetch the student's exercises for this course
            exercises = Exercise.query.filter_by(course_id=course.id, student_username=username).all()

            # Format the exercises
            exercises_data = [{
                'id': exercise.id,
                'exercise_name': exercise.name,
                'grade_result': exercise.grade_result,
                'feedback': exercise.feedback,  # Include feedback field
                'due_date': exercise.due_date.isoformat(),
                'submitted_at': exercise.submitted_at.isoformat() if exercise.submitted_at else None
            } for exercise in exercises]

            # Format the course data
            course_data = {
                'course_id': course.id,
                'course_name': course.name,
                'owner': {
                    'id': instructor.username,
                    'name': instructor.name
                },
                'students': [{
                    'id': username,
                    'name': User.query.filter_by(username=username).first().name,  # Fetch the student's name
                    'exercises': exercises_data
                }]
            }
            courses_data.append(course_data)

        return jsonify(courses_data), 200

    except Exception as e:
        logging.error(f"An error occurred while fetching courses: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
