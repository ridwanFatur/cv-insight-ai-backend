from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.user import User
from utils.email_utils import is_valid_email


def get_or_create_user(db: Session, email: str, name: str):
    user = db.query(User).filter(User.email == email).first()
    if user:
        return user, False
    if not is_valid_email(email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Email Format"
        )
    new_user = User(name=name, email=email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user, True


def get_user(db: Session, id: int) -> User:
    user = db.query(User).filter(User.id == id).first()
    if user:
        return user

    return None
