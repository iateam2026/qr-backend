from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "QR Backend")
    ENV: str = os.getenv("ENV", "dev")
    ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "http://localhost:4200")

    FIREBASE_CREDENTIALS: str = os.getenv("FIREBASE_CREDENTIALS", "serviceAccountKey.json")
    FIREBASE_STORAGE_BUCKET: str = os.getenv("FIREBASE_STORAGE_BUCKET", "")

settings = Settings()
