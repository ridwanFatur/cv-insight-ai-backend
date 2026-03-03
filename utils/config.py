from dotenv import load_dotenv
import os

load_dotenv()

CORS_ORIGINS = os.getenv("CORS_ORIGINS")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
PROJECT_ID = os.getenv("PROJECT_ID")
GOOGLE_BUCKET_NAME = os.getenv("GOOGLE_BUCKET_NAME")
