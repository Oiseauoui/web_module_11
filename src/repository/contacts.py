from datetime import date
from sqlalchemy import extract
from sqlalchemy.orm import Session
from src.database.models import Contact
from src.schemas import ContactModel


async def get_contacts(db: Session):
    contacts = db.query(Contact).all()
    return contacts


async def get_contact(contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    return contact


async def get_contact_by_id(contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    return contact


async def get_contact_by_email(email: str, db: Session):
    contact = db.query(Contact).filter_by(email=email).first()
    return contact


async def get_contact_by_lastname(lastname: str, db: Session):
    contact = db.query(Contact).filter_by(lastname=lastname).first()
    return contact


async def create(body: ContactModel, db: Session):
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update(contact_id: int, body: ContactModel, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        contact.lastname = body.lastname
        contact.telephone = body.telephone
        contact.date_birthday = body.date_birthday
        contact.description = body.description
        contact.email = body.email
        db.commit()
    return contact


async def remove(contact_id: int, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def get_contacts_birthday(start_date: date, end_date: date, db: Session):
    birth_day = extract('day', Contact.date_birthday)
    birth_month = extract('month', Contact.date_birthday)
    contacts = db.query(Contact).filter(
        birth_month == extract('month', start_date),
        birth_day.between(extract('day', start_date), extract('day', end_date))
    ).all()
    return contacts
