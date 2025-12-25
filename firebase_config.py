import firebase_admin
from firebase_admin import credentials, firestore, storage
from config import settings

_db = None

def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS)
        firebase_admin.initialize_app(cred, {
            "storageBucket": settings.FIREBASE_STORAGE_BUCKET
        })

def get_db():
    global _db
    init_firebase()
    if _db is None:
        _db = firestore.client()
    return _db

def get_bucket():
    init_firebase()
    return storage.bucket()
