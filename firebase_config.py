import os
import firebase_admin
from firebase_admin import credentials, firestore, storage
from config import settings

_db = None

def init_firebase():
    """
    Init Firebase Admin once.

    ✅ En local: utilise un fichier service account JSON si FIREBASE_CREDENTIALS existe.
    ✅ En Cloud Run: si le fichier n'existe pas, initialise via le Service Account du runtime (recommandé).
    """
    if firebase_admin._apps:
        return

    # Bucket (optionnel mais recommandé si tu utilises Storage)
    bucket = getattr(settings, "FIREBASE_STORAGE_BUCKET", "") or os.getenv("FIREBASE_STORAGE_BUCKET", "")

    cred_path = getattr(settings, "FIREBASE_CREDENTIALS", "") or os.getenv("FIREBASE_CREDENTIALS", "")

    # 1) Mode LOCAL: fichier JSON présent
    if cred_path and os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred, {"storageBucket": bucket} if bucket else None)
        return

    # 2) Mode CLOUD RUN / PROD: pas de fichier -> utilise les credentials du runtime
    # (Service Account Cloud Run + IAM permissions)
    firebase_admin.initialize_app(options={"storageBucket": bucket} if bucket else None)


def get_db():
    """Retourne le client Firestore (singleton)."""
    global _db
    init_firebase()
    if _db is None:
        _db = firestore.client()
    return _db


def get_bucket():
    """Retourne le bucket Storage (si configuré)."""
    init_firebase()
    return storage.bucket()
