from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from firebase_admin import firestore

from firebase_config import get_db, get_bucket
from models.qr_models import QRCreate, QRBulkCreate, QRUpdate

import shortuuid
import qrcode
from io import BytesIO
from datetime import datetime, timezone

router = APIRouter(prefix="/qr", tags=["QR"])

# ⚠️ IMPORTANT :
# - Sur PC: http://127.0.0.1:8000
# - Sur téléphone (même Wi-Fi): remplace par l'IP de ton PC ex: http://192.168.0.10:8000
# - En prod: https://qr.ia2team.com
BASE_SCAN_URL = "http://192.168.18.8:8000/qr/scan"

def now_iso():
    return datetime.now(timezone.utc).isoformat()

def make_qr_png(data: str) -> bytes:
    img = qrcode.make(data)
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def upload_to_storage(path: str, content: bytes) -> str:
    bucket = get_bucket()
    blob = bucket.blob(path)
    blob.upload_from_string(content, content_type="image/png")
    blob.make_public()
    return blob.public_url


@router.post("/create")
def create_qr(payload: QRCreate):
    db = get_db()
    code = shortuuid.ShortUUID().random(length=8)

    scan_url = f"{BASE_SCAN_URL}/{code}"
    png = make_qr_png(scan_url)

    storage_path = f"qr_codes/{code}.png"
    try:
        qr_image_url = upload_to_storage(storage_path, png)
    except Exception:
        qr_image_url = None  # still works without storage

    doc = {
        "code": code,
        "name": payload.name or f"QR-{code}",
        "target_url": str(payload.target_url),
        "scan_url": scan_url,
        "qr_image_url": qr_image_url,
        "is_active": True,
        "created_at": now_iso(),
        "scan_count": 0
    }

    db.collection("qr_codes").document(code).set(doc)
    return doc


@router.post("/bulk")
def bulk_create(payload: QRBulkCreate):
    db = get_db()
    results = []

    for item in payload.items:
        code = shortuuid.ShortUUID().random(length=8)
        scan_url = f"{BASE_SCAN_URL}/{code}"
        png = make_qr_png(scan_url)

        storage_path = f"qr_codes/{code}.png"
        try:
            qr_image_url = upload_to_storage(storage_path, png)
        except Exception:
            qr_image_url = None

        doc = {
            "code": code,
            "name": item.name or f"QR-{code}",
            "target_url": str(item.target_url),
            "scan_url": scan_url,
            "qr_image_url": qr_image_url,
            "is_active": True,
            "created_at": now_iso(),
            "scan_count": 0
        }

        db.collection("qr_codes").document(code).set(doc)
        results.append(doc)

    return {"count": len(results), "items": results}


@router.get("/list")
def list_qr():
    db = get_db()
    docs = db.collection("qr_codes").stream()
    return [d.to_dict() for d in docs]


@router.put("/update/{code}")
def update_qr(code: str, payload: QRUpdate):
    db = get_db()
    ref = db.collection("qr_codes").document(code)
    doc = ref.get()
    if not doc.exists:
        raise HTTPException(404, "NOT_FOUND")

    data = {k: v for k, v in payload.model_dump().items() if v is not None}
    if not data:
        raise HTTPException(400, "NO_DATA")

    ref.set(data, merge=True)
    return {"ok": True, "code": code, "updated": data}


@router.delete("/delete/{code}")
def delete_qr(code: str):
    db = get_db()
    ref = db.collection("qr_codes").document(code)
    doc = ref.get()
    if not doc.exists:
        raise HTTPException(404, "NOT_FOUND")

    ref.delete()
    return {"ok": True, "deleted": code}


@router.get("/scan/{code}")
def scan(code: str, request: Request):
    db = get_db()

    qr_ref = db.collection("qr_codes").document(code)
    qr_doc = qr_ref.get()
    if not qr_doc.exists:
        raise HTTPException(404, "QR_NOT_FOUND")

    qr = qr_doc.to_dict() or {}
    if not qr.get("is_active", True):
        raise HTTPException(403, "QR_DISABLED")

    target_url = qr.get("target_url")
    if not target_url:
        raise HTTPException(500, "TARGET_URL_MISSING")

    # ✅ increment scan_count (atomic, safe)
    qr_ref.update({"scan_count": firestore.Increment(1)})

    # log scan details
    scan_log = {
        "code": code,
        "scanned_at": now_iso(),
        "ip": request.client.host if request.client else None,
        "user_agent": request.headers.get("user-agent"),
        "referrer": request.headers.get("referer"),
        "accept_language": request.headers.get("accept-language"),
    }
    db.collection("qr_scans").add(scan_log)

    # ✅ real redirect
    return RedirectResponse(url=target_url, status_code=302)


@router.get("/stats/global")
def global_stats():
    db = get_db()
    docs = db.collection("qr_codes").stream()
    total_codes = 0
    total_scans = 0
    for d in docs:
        total_codes += 1
        total_scans += int((d.to_dict() or {}).get("scan_count", 0))
    return {"total_codes": total_codes, "total_scans": total_scans}


@router.get("/stats/{code}")
def code_stats(code: str):
    db = get_db()
    doc = db.collection("qr_codes").document(code).get()
    if not doc.exists:
        raise HTTPException(404, "NOT_FOUND")
    return doc.to_dict()
