from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import auth, cv_feedback, user, user_token
from fastapi import FastAPI

from rabbitmq.constants import CV_REVIEW_RESULTS
from rabbitmq.consumer.cv_review_consumer import cv_review_callback
from utils.config import CORS_ORIGINS
import logging
from contextlib import asynccontextmanager
import threading
from rabbitmq.channel_client import mq_channel_client


def app_consumer():
    mq_channel_client.basic_qos(prefetch_count=1)
    mq_channel_client.basic_consume(
        queue=CV_REVIEW_RESULTS,
        on_message_callback=cv_review_callback,
    )

    mq_channel_client.start_consuming()


@asynccontextmanager
async def lifespan(app: FastAPI):
    thread = threading.Thread(target=app_consumer, daemon=True)
    thread.start()
    print("Start Consuming")
    yield

app = FastAPI(
    title="CV Insight AI",
    version="1.0.0", redirect_slashes=False,
    lifespan=lifespan
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in CORS_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "App is Ready"}

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(user_token.router)
app.include_router(cv_feedback.router)
