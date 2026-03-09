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


def consume_user_token_credit(db: Session, user_id: int, action):
    user_token = db.query(UserToken).filter(
        UserToken.user_id == user_id
    ).first()

    if not user_token:
        raise HTTPException(
            status_code=404,
            detail="User token not found"
        )

    if user_token.total_tokens <= 0:
        raise HTTPException(
            status_code=400,
            detail="Out of token"
        )

    user_token.total_tokens -= 1
    db.commit()
    db.refresh(user_token)

    try:
        action()
    except Exception as e:
        user_token.total_tokens += 1
        db.commit()
        db.refresh(user_token)
        raise e

    return user_token.total_tokens
