from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config import settings
from cors import setup_cors
from routers.qr_router import router as qr_router

app = FastAPI(title=settings.PROJECT_NAME)

setup_cors(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(qr_router)

@app.get("/")
def root():
    return {"message": "QR Backend Running ✅", "project": settings.PROJECT_NAME}
