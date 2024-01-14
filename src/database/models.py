from pydantic import validator
from sqlalchemy import Column, Integer, String, DateTime, func, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


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
