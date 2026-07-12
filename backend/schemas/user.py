from pydantic import BaseModel, EmailStr, Field
from models.enums import UserRole


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=8)

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRoleUpdate(BaseModel):
    role: UserRole