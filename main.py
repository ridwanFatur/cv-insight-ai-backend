from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from api import auth, user
from fastapi import FastAPI

from db.database import Base, engine
from utils.config import CORS_ORIGINS


app = FastAPI(title="CV Insight AI",
              version="1.0.0", redirect_slashes=False)


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
