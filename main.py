from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config import settings
from routers.qr_router import router as qr_router

app = FastAPI(title=settings.PROJECT_NAME)

# CORS (PROPRE & PROD)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,  # ✅ depuis config.py
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes QR
app.include_router(qr_router)

# Root
@app.get("/")
def root():
    return {
        "message": "QR Backend Running ✅",
        "project": settings.PROJECT_NAME
    }

# Health check (Cloud Run / monitoring)
@app.get("/health")
def health():
    return {
        "status": "ok",
        "env": settings.ENV
    }
