from datetime import datetime, timedelta
from typing import List
from fastapi import Depends, HTTPException, status, Path, APIRouter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.repository import contacts as repository_contacts
from src.schemas import ContactResponse
from src.schemas import ContactModel


router = APIRouter(prefix="/contacts", tags=['contacts'])


@router.get("/", response_model=List[ContactResponse], name="Повернути список власників")
async def get_contacts(db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse, name="Отримати один контакт за ідентифікатором")
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_id(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.get("/by_lastname/{lastname}", response_model=ContactResponse, name="Пошук по імені")
async def get_contact(lastname: str, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_lastname(lastname, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.get("/by_email/{email}", response_model=ContactResponse, name="Пошук по email")
async def get_contact(email: str, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_email(email, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED, name="Створити новий контакт")
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_email(body.email, db)
    if contact:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email is exists!')

    contact = await repository_contacts.create(body, db)

    return contact


@router.put("/{contact_id}", response_model=ContactResponse, name="Оновити існуючий контакт")
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.update(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")

    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT, name="Видалити контакт")
async def remove_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.remove(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")

    return contact


@router.get("/birthday-list/", response_model=list[ContactResponse], name="Список контактів з днями народження на найближчі 7 днів.")
async def get_birthday_list_contact(db: Session = Depends(get_db)):
    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=7)
    contacts = await repository_contacts.get_contacts_birthday(start_date, end_date, db)
    return contacts
