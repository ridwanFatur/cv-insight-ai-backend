from fastapi import APIRouter, UploadFile, File, Depends, Request
from db.database import get_db
from dependencies.auth_middleware import get_current_user_id
from services.cv_feedback_service import get_cv_detail, get_cv_feedback, upload_cv_to_gcs
from sqlalchemy.orm import Session
from functools import partial

from services.user_token_service import consume_user_token_credit

router = APIRouter(
    prefix="/api/cv-feedback",
    tags=["user"],
    dependencies=[Depends(get_current_user_id)]
)


@router.get("/")
def fetch_cv_feedback(
    request: Request,
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
):
    return get_cv_feedback(
        db=db,
        user_id=request.state.user_id,
        page=page,
        page_size=page_size,
    )


@router.get("/{id}")
def fetch_detail_cv_feedback(
    id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    return get_cv_detail(
        db=db,
        user_id=request.state.user_id,
        id=id,
    )


@router.post("/upload")
def upload_cv(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    user_id = request.state.user_id
    remaining_tokens = consume_user_token_credit(
        db,
        user_id,
        partial(upload_cv_to_gcs, db, user_id, file)
    )
    return {
        "remaining_tokens": remaining_tokens
    }
