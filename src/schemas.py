from datetime import datetime, date

from pydantic import BaseModel, Field, EmailStr


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
