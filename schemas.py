import datetime
from pydantic import BaseModel
from typing import List, Optional


# --- ADMIN GATEWAY BLUEPRINTS ---
class AuthRequest(BaseModel):
    passcode: str


# --- CATALOG LISTINGS BLUEPRINTS ---
class ListingBase(BaseModel):
    type: str          # Matches front-end options: 'App', 'Website', 'CRM'
    status: str        # Matches front-end options: 'Live', 'InDev', 'Concept'
    title: str
    tagline: str
    desc: str
    stack: List[str]   # Explicit list wrapper handling array inputs (e.g. ["Next.js", "FastAPI"])
    sku: str
    previewType: str   # Matches front-end: 'image' or 'iframe'
    link: Optional[str] = ""
    previewUrl: str
    featured: bool


class ListingCreate(ListingBase):
    id: Optional[str] = None  # Auto-generated if not supplied by the frontend


class ListingUpdate(BaseModel):
    # All fields optional so PATCH-style partial edits work from the admin dashboard.
    type: Optional[str] = None
    status: Optional[str] = None
    title: Optional[str] = None
    tagline: Optional[str] = None
    desc: Optional[str] = None
    stack: Optional[List[str]] = None
    sku: Optional[str] = None
    previewType: Optional[str] = None
    link: Optional[str] = None
    previewUrl: Optional[str] = None
    featured: Optional[bool] = None


class ListingResponse(ListingBase):
    id: str
    created_at: Optional[datetime.datetime] = None

    class Config:
        from_attributes = True


# --- CLIENT MESSAGES BLUEPRINTS ---
class MessageCreate(BaseModel):
    name: str
    email: str
    interest: str
    message: str


class MessageResponse(MessageCreate):
    id: str
    timestamp: str
    read: bool

    class Config:
        from_attributes = True
