from pydantic import BaseModel, Field
import uuid
from datetime import datetime


class UserCreateModel(BaseModel):
    username: str = Field(max_length=8, description="Username is Required")
    email: str = Field(max_length=25, description="email is required")
    password: str = Field(min_length=6)
    
    
