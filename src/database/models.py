# database/models.py
import enum
from pydantic import validator
from sqlalchemy import Column, Integer, String, DateTime, func, Date, Enum, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Role(enum.Enum):
    admin: str = 'admin'
    moderator: str = 'moderator'
    user: str = 'user'


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    lastname = Column(String(255), index=True)
    telephone = Column(String(15), index=True)
    date_birthday = Column(Date)
    description = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    @validator("telephone")
    def validate_telephone(cls, value):
        # Перетворюємо формат телефонного номера, якщо це потрібно
        if value.startswith("0"):
            value = "+38" + value
        return value

    @validator("telephone")
    def check_telephone_format(cls, value):
        # Валідація формату телефонного номера
        if not value.startswith("+38") or not value[1:].isdigit():
            raise ValueError("Invalid telephone number format. Use either +380507380560 or 0507380560.")
        return value


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    refresh_token = Column(String(255), nullable=True)
    avatar = Column(String(255), nullable=True)
    roles = Column('roles', Enum(Role), default=Role.user)
    email_verified = Column(Boolean, default=False)
