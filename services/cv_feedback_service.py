from sqlalchemy.orm import Session
from sqlalchemy import desc
from models.cv_feedback import CVFeedback
from fastapi import HTTPException, UploadFile
from google.cloud import storage
import uuid
from models.user_token import UserToken
from utils.config import GOOGLE_BUCKET_NAME, PROJECT_ID
from datetime import timedelta
from vertexai.generative_models import GenerativeModel, Part, GenerationConfig
import logging

logger = logging.getLogger(__name__)


def get_cv_detail(
    db: Session,
    user_id: int,
    id: int
):
    cv = db.query(CVFeedback).filter(
        CVFeedback.user_id == user_id,
        CVFeedback.id == id
    ).first()

    if not cv:
        raise HTTPException(
            status_code=404,
            detail="CV not found"
        )

    logger.info("CV with ID existed")

    prefix = f"https://storage.googleapis.com/{GOOGLE_BUCKET_NAME}/"

    if not cv.file_link.startswith(prefix):
        raise HTTPException(
            status_code=400,
            detail="Invalid file link"
        )
    object_name = cv.file_link.replace(prefix, "")

    client = storage.Client(project=PROJECT_ID)
    bucket = client.bucket(GOOGLE_BUCKET_NAME)
    blob = bucket.blob(object_name)
    signed_url = blob.generate_signed_url(
        version="v4",
        expiration=timedelta(minutes=15),
        method="GET",
    )
    return {
        "cv_feedback": cv,
        "download_url": signed_url
    }


def get_cv_feedback(
    db: Session,
    user_id: int,
    page: int = 1,
    page_size: int = 10,
):
    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 10

    offset = (page - 1) * page_size

    query = db.query(CVFeedback).filter(CVFeedback.user_id == user_id)

    total = query.count()
    items = (
        query
        .order_by(desc(CVFeedback.created_at))
        .offset(offset)
        .limit(page_size)
        .all()
    )

    total_pages = (total + page_size - 1) // page_size

    return {
        "data": items,
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": total_pages,
    }


def upload_cv_and_create_feedback(
    db: Session,
    user_id: int,
    file: UploadFile,
):
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

    logger.info("Process Upload CV")

    # Upload to GCS
    logger.info("Process Upload CV to GCS")
    file.file.seek(0)

    client = storage.Client(project=PROJECT_ID)
    bucket = client.bucket(GOOGLE_BUCKET_NAME)

    file_extension = file.filename.split(".")[-1]
    unique_filename = f"cv/{user_id}/{uuid.uuid4()}.{file_extension}"

    blob = bucket.blob(unique_filename)

    blob.upload_from_file(
        file.file,
        content_type=file.content_type,
    )
    file_url = f"https://storage.googleapis.com/{GOOGLE_BUCKET_NAME}/{unique_filename}"

    # Use Gemini
    logger.info("Process Analsys by Gemini")
    model = GenerativeModel("gemini-2.5-flash")
    gcs_uri = f"gs://{GOOGLE_BUCKET_NAME}/{unique_filename}"
    pdf_file = Part.from_uri(
        uri=gcs_uri,
        mime_type="application/pdf"
    )
    prompt = """
			Please review the attached file and determine whether it is a CV/resume. 
			If it is a CV, provide detailed and constructive suggestions on what can be improved 
			(e.g., structure, clarity, formatting, wording, achievements, skills section, consistency, etc.). 
			Match the language of your response to the primary language used in the CV. 
			If the uploaded file is NOT a CV/resume, clearly state that this application is only intended for CV review.
    """
    config = GenerationConfig(
        temperature=0.7,
        max_output_tokens=500
    )
    response = model.generate_content(
        [pdf_file, prompt],
        generation_config=config
    )
    feedback = response.text

    # Save on DB
    cv_feedback = CVFeedback(
        user_id=user_id,
        file_link=file_url,
        feedback=feedback,
    )

    db.add(cv_feedback)
    user_token.total_tokens -= 1

    db.commit()
    db.refresh(cv_feedback)
    db.refresh(user_token)

    return cv_feedback, user_token.total_tokens
