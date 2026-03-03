from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.user_token import UserToken


def get_user_token(db: Session, user_id: int):
    user_token = (
        db.query(UserToken)
        .filter(UserToken.user_id == user_id)
        .first()
    )

    if not user_token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User token not found"
        )

    return user_token.total_tokens
