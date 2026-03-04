from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from api import auth, cv_feedback, user, user_token
from fastapi import FastAPI

# Register Model
from models.user import User
from models.user_token import UserToken
from models.cv_feedback import CVFeedback

from db.database import Base, engine
from utils.config import CORS_ORIGINS
import logging

app = FastAPI(title="CV Insight AI",
              version="1.0.0", redirect_slashes=False)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

Base.metadata.create_all(bind=engine)

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
