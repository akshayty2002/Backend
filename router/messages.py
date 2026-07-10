import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from router.auth import verify_admin_token
from notifications import send_new_message_notification

router = APIRouter(prefix="/api/messages", tags=["Client Pipeline Inbox Requests"])


@router.get("", response_model=List[schemas.MessageResponse])
def get_inbox_messages(db: Session = Depends(get_db), auth=Depends(verify_admin_token)):
    return db.query(models.Message).order_by(models.Message.timestamp.desc()).all()


@router.post("")
def transmit_client_message(payload: schemas.MessageCreate, db: Session = Depends(get_db)):
    generated_id = f"msg-{int(datetime.datetime.now().timestamp())}"
    current_time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_message = models.Message(
        id=generated_id, name=payload.name, email=payload.email,
        interest=payload.interest, message=payload.message,
        timestamp=current_time_str, read=False
    )
    db.add(new_message)
    db.commit()

    # Best-effort email alert — never blocks or fails the actual submission.
    send_new_message_notification(new_message)

    return {"success": True, "id": generated_id}


@router.patch("/{message_id}/read")
def mark_message_read(
    message_id: str,
    db: Session = Depends(get_db),
    auth=Depends(verify_admin_token),
):
    msg = db.query(models.Message).filter(models.Message.id == message_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found.")
    msg.read = True
    db.commit()
    return {"status": "ok", "id": message_id, "read": True}


@router.delete("/{message_id}")
def delete_message(
    message_id: str,
    db: Session = Depends(get_db),
    auth=Depends(verify_admin_token),
):
    msg = db.query(models.Message).filter(models.Message.id == message_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found.")
    db.delete(msg)
    db.commit()
    return {"status": "deleted", "id": message_id}
