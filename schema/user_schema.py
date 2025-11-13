from pydantic import BaseModel, Field
import uuid
from datetime import datetime


class UserCreateModel(BaseModel):
    username: str = Field(max_length=8, description="Username is Required")
    email: str = Field(max_length=25, description="email is required")
    password: str = Field(min_length=6)


class UserLoginModel(BaseModel):
    email: str = Field(max_length=25, description="email is required")
    password: str = Field(min_length=6)




class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    password: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime
