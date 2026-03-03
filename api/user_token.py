from fastapi import APIRouter, Depends, Request
from db.database import get_db
from dependencies.auth_middleware import get_current_user_id
from services.user_token_service import get_user_token
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/api/user-token",
    tags=["user"],
    dependencies=[Depends(get_current_user_id)]
)


@router.get("/")
async def fetch_user_token(request: Request, db: Session = Depends(get_db)):
    total_tokens = get_user_token(db, request.state.user_id)
    return {
        "total_tokens": total_tokens
    }
