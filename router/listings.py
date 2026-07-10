import json
import uuid
import datetime
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

import models
import schemas
from database import get_db
from router.auth import verify_admin_token

router = APIRouter(prefix="/api/listings", tags=["listings"])


def _serialize(listing: models.Listing) -> dict:
    return {
        "id": listing.id,
        "type": listing.type,
        "status": listing.status,
        "title": listing.title,
        "tagline": listing.tagline,
        "desc": listing.desc,
        "stack": json.loads(listing.stack) if listing.stack else [],
        "sku": listing.sku,
        "previewType": listing.previewType,
        "link": listing.link,
        "previewUrl": listing.previewUrl,
        "featured": bool(listing.featured),
        "created_at": listing.created_at,
    }


@router.get("")
def get_listings(
    db: Session = Depends(get_db),
    q: Optional[str] = Query(None, description="Search title, tagline, description, stack, sku"),
    type: Optional[str] = Query(None, description="Filter by type: App, Website, CRM"),
    status: Optional[str] = Query(None, description="Filter by status: Live, InDev, Concept"),
    featured: Optional[bool] = Query(None),
    sort: str = Query("newest", description="newest | oldest | title_asc | title_desc"),
):
    """
    Returns only listings that actually exist in the database — no mock or
    fallback data. Supports optional search, filtering, and sorting so the
    catalog page can offer a real browsing experience.
    """
    query = db.query(models.Listing)

    if type:
        query = query.filter(models.Listing.type == type)
    if status:
        query = query.filter(models.Listing.status == status)
    if featured is not None:
        query = query.filter(models.Listing.featured == featured)
    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(
                models.Listing.title.ilike(like),
                models.Listing.tagline.ilike(like),
                models.Listing.desc.ilike(like),
                models.Listing.stack.ilike(like),
                models.Listing.sku.ilike(like),
            )
        )

    if sort == "oldest":
        query = query.order_by(models.Listing.created_at.asc())
    elif sort == "title_asc":
        query = query.order_by(models.Listing.title.asc())
    elif sort == "title_desc":
        query = query.order_by(models.Listing.title.desc())
    else:  # newest (default)
        query = query.order_by(models.Listing.created_at.desc())

    return [_serialize(l) for l in query.all()]


@router.get("/{listing_id}")
def get_listing(listing_id: str, db: Session = Depends(get_db)):
    listing = db.query(models.Listing).filter(models.Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found.")
    return _serialize(listing)


@router.post("", status_code=201)
def create_listing(
    payload: schemas.ListingCreate,
    db: Session = Depends(get_db),
    auth=Depends(verify_admin_token),
):
    listing_id = payload.id or f"lst-{uuid.uuid4().hex[:10]}"

    if db.query(models.Listing).filter(models.Listing.id == listing_id).first():
        raise HTTPException(status_code=409, detail="A listing with this id already exists.")

    if payload.sku and db.query(models.Listing).filter(models.Listing.sku == payload.sku).first():
        raise HTTPException(status_code=409, detail="A listing with this SKU already exists.")

    listing = models.Listing(
        id=listing_id,
        type=payload.type,
        status=payload.status,
        title=payload.title,
        tagline=payload.tagline,
        desc=payload.desc,
        stack=json.dumps(payload.stack),
        sku=payload.sku,
        previewType=payload.previewType,
        link=payload.link,
        previewUrl=payload.previewUrl,
        featured=payload.featured,
        created_at=datetime.datetime.utcnow(),
    )
    db.add(listing)
    db.commit()
    db.refresh(listing)
    return _serialize(listing)


@router.put("/{listing_id}")
def update_listing(
    listing_id: str,
    payload: schemas.ListingUpdate,
    db: Session = Depends(get_db),
    auth=Depends(verify_admin_token),
):
    listing = db.query(models.Listing).filter(models.Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found.")

    data = payload.model_dump(exclude_unset=True)

    if "sku" in data and data["sku"] and data["sku"] != listing.sku:
        clash = db.query(models.Listing).filter(
            models.Listing.sku == data["sku"], models.Listing.id != listing_id
        ).first()
        if clash:
            raise HTTPException(status_code=409, detail="A listing with this SKU already exists.")

    if "stack" in data:
        data["stack"] = json.dumps(data["stack"])

    for field, value in data.items():
        setattr(listing, field, value)

    db.commit()
    db.refresh(listing)
    return _serialize(listing)


@router.delete("/{listing_id}")
def delete_listing(
    listing_id: str,
    db: Session = Depends(get_db),
    auth=Depends(verify_admin_token),
):
    listing = db.query(models.Listing).filter(models.Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found.")
    db.delete(listing)
    db.commit()
    return {"status": "deleted", "id": listing_id}
