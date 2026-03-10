import hashlib

from sqlalchemy.orm import Session
from sqlalchemy import desc
from models.cv_feedback import CVFeedback
from fastapi import HTTPException, UploadFile
from google.cloud import storage
import uuid
from rabbitmq.publisher.cv_review_publisher import cv_review_publish
from utils.config import GOOGLE_BUCKET_NAME, PROJECT_ID
from datetime import timedelta
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


def submit_cv_for_review(
    db: Session,
    user_id: int,
    file: UploadFile,
):
    logger.info("Process Upload CV to GCS")
    file.file.seek(0)

    file_bytes = file.file.read()
    file_hash = hashlib.sha256(file_bytes).hexdigest()

    file.file.seek(0)
    existing = (
        db.query(CVFeedback)
        .filter(CVFeedback.file_hash == file_hash)
        .first()
    )
    if existing:
        logger.info("File already exists, reuse link")
        file_url = existing.file_link
    else:
        logger.info("Uploading new file to GCS")

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

    # Save on DB
    cv_feedback = CVFeedback(
        user_id=user_id,
        file_link=file_url,
        file_hash=file_hash,
        status="loading"
    )
    db.add(cv_feedback)
    db.commit()
    db.refresh(cv_feedback)

    cv_review_publish(cv_feedback.id, user_id)
