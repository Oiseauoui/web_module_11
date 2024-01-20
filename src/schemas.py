from datetime import datetime, date

from pydantic import BaseModel, Field, EmailStr

from src.database.models import Role


class ContactModel(BaseModel):
    id: int
    email: EmailStr
    lastname: str = Field('Iulia', min_length=3, max_length=16)
    telephone: str
    date_birthday: date
    description: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime


class ContactResponse(BaseModel):
    id: int = 1
    email: EmailStr
    lastname: str
    telephone: str
    date_birthday: date
    description: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    username: str = Field(min_length=2, max_length=50)
    password: str = Field(min_length=6, max_length=50)
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    avatar: str
    roles: Role

    class Config:
        orm_mode = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
