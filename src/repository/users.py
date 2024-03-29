# repository/users.py
from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User | None:
    return db.query(User).filter_by(email=email).first()


async def create_user(body: UserModel, db: Session):
    grav = Gravatar(body.email)
    new_user = User(**body.dict(), avatar=grav.get_image())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, refresh_token, db: Session):
    user.refresh_token = refresh_token
    db.commit()

async def create_user(body: UserModel, db: Session):
    grav = Gravatar(body.email)
    avatar_url = grav.get_image()

    # Upload avatar to Cloudinary
    response = cloudinary.uploader.upload(avatar_url)
    cloudinary_url = response['secure_url']

    new_user = User(**body.dict(), avatar=cloudinary_url)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
