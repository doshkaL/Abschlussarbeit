
from pydantic import BaseModel, Field

class UserDTO(BaseModel):
    username: str = Field( description="Unique identifier for the user")
    name: str
    password: str
    role: str = Field(description="Role of the user, either 'student' or 'instructor'")
   