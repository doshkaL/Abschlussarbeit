from models import User, Course, Exercise
from dto_models import UserDTO, CourseDTO, ExerciseDTO


# Mapper: SQLAlchemy -> DTO
def user_to_dto(user: User) -> UserDTO:
    return UserDTO(
        username=user.username,
        name=user.name,
        password=user.password,
        role=user.role,
        created_at=user.created_at,
        updated_at=user.updated_at
    )


def course_to_dto(course: Course) -> CourseDTO:
    return CourseDTO(
        id=course.id,
        name=course.name,
        instructor_username=course.instructor_username,
        created_at=course.created_at,
        updated_at=course.updated_at
    )


def exercise_to_dto(exercise: Exercise) -> ExerciseDTO:
    return ExerciseDTO(
        id=exercise.id,
        name=exercise.name,
        course_id=exercise.course_id,
        student_username=exercise.student_username,
        feedback=exercise.feedback,
        grade_result=exercise.grade_result,
        due_date=exercise.due_date,
        submitted_at=exercise.submitted_at
    )


# Mapper: DTO -> SQLAlchemy
def dto_to_user(dto: UserDTO) -> User:
    return User(
        username=dto.username,
        name=dto.name,
        password=dto.password, 
        role=dto.role,
        created_at=dto.created_at,
        updated_at=dto.updated_at
    )


def dto_to_course(dto: CourseDTO) -> Course:
    return Course(
        id=dto.id,
        name=dto.name,
        instructor_username=dto.instructor_username,
        created_at=dto.created_at,
        updated_at=dto.updated_at
    )


def dto_to_exercise(dto: ExerciseDTO) -> Exercise:
    return Exercise(
        id=dto.id,
        name=dto.name,
        course_id=dto.course_id,
        student_username=dto.student_username,
        feedback=dto.feedback,
        grade_result=dto.grade_result,
        due_date=dto.due_date,
        submitted_at=dto.submitted_at
    )
def user_dto_to_model(user_dto):
    return User(
        username=user_dto.username,
        name=user_dto.name,
        password=user_dto.password,
        role=user_dto.role,
        created_at=user_dto.created_at,
        updated_at=user_dto.updated_at
    )
