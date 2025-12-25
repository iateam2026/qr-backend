from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from config import settings

def setup_cors(app: FastAPI):
    origins = [o.strip() for o in settings.ALLOWED_ORIGINS.split(",") if o.strip()]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins if origins else ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
