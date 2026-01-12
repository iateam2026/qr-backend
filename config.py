from typing import List
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class Settings(BaseSettings):
    # App
    PROJECT_NAME: str = "QR Backend"
    ENV: str = "dev"

    # CORS (liste)
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:4200",
        "http://localhost:3000",
        "https://ia2team.com",
        "https://qrcode.ia2team.com",
    ]

    # Firebase
    FIREBASE_CREDENTIALS: str = ""
    FIREBASE_STORAGE_BUCKET: str = ""

    # ✅ Pydantic v2 config
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )

settings = Settings()
