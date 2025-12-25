from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config import settings
from cors import setup_cors
from routers.qr_router import router as qr_router

app = FastAPI(title=settings.PROJECT_NAME)

# Optionnel: ton helper CORS (si tu l'utilises déjà)
setup_cors(app)

# CORS (OK pour dashboard + tests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tu peux remplacer par settings.ALLOWED_ORIGINS plus tard
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes QR
app.include_router(qr_router)

@app.get("/")
def root():
    return {"message": "QR Backend Running ✅", "project": settings.PROJECT_NAME}

@app.get("/health")
def health():
    return {"status": "ok", "env": settings.ENV}
