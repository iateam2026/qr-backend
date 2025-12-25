from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

class QRCreate(BaseModel):
    target_url: HttpUrl
    name: Optional[str] = None

class QRBulkCreate(BaseModel):
    items: List[QRCreate] = Field(min_length=1, max_length=100)

class QRUpdate(BaseModel):
    name: Optional[str] = None
    target_url: Optional[HttpUrl] = None
    is_active: Optional[bool] = None
