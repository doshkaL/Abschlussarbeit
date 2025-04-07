from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import uuid


class UserDTO(BaseModel):
    username: str = Field( description="Unique identifier for the user")
    name: str
    password: str
    role: str = Field(description="Role of the user, either 'student' or 'instructor'")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Timestamp when the user was created")
    updated_at: Optional[datetime] = Field(default=None, description="Timestamp when the user was last updated")


class CourseDTO(BaseModel):
    id: str = Field( description="Unique identifier for the course")
    name: str
    instructor_username: str = Field(description="Username of the instructor responsible for the course")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Timestamp when the course was created")
    updated_at: Optional[datetime] = Field(default=None, description="Timestamp when the course was last updated")


class ExerciseDTO(BaseModel):
    id: str = Field( description="Unique identifier for the exercise")
    name: str
    course_id: str = Field(description="Identifier for the course associated with the exercise")
    student_username: str = Field(description="Username of the student who submitted the exercise")
    feedback: Optional[str] = Field(default=None, description="Feedback given for the exercise")
    grade_result: Optional[str] = Field(default=None, description="Detailed grade results for the exercise in text format")
    due_date: datetime
    submitted_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Timestamp when the exercise was submitted")
