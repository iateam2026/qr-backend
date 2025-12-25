from pydantic import BaseSettings
from typing import List
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # App
    PROJECT_NAME: str = "QR Backend"
    ENV: str = "dev"

    # CORS (liste, pas string)
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:4200",
        "http://localhost:3000",
        "https://ia2team.com",
        "https://qrcode.ia2team.com",
    ]

    # Firebase
    # En local : serviceAccountKey.json
    # En Cloud Run : laisser vide (Service Account du runtime)
    FIREBASE_CREDENTIALS: str = ""
    FIREBASE_STORAGE_BUCKET: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
