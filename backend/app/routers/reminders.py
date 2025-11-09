# app/routers/reminders.py
from fastapi import APIRouter, Request, HTTPException, Depends
from sqlmodel import Session, select
from ..models.reminder import Reminder
from ..database import get_session
from datetime import datetime

router = APIRouter(prefix="/reminders", tags=["reminders"])

def get_user_id_from_request(request: Request):
    auth = request.headers.get("authorization")
    if not auth:
        raise HTTPException(status_code=401, detail="Missing auth")
    token = auth.split(" ")[1]
    from ..utils.security import decode_token
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return int(payload.get("sub"))

@router.post("/schedule")
def schedule(payload: dict, request: Request, session: Session = Depends(get_session)):
    """
    payload: {"related_type":"tax","related_id":12,"remind_at":"2024-12-10T10:00:00"}
    """
    user_id = get_user_id_from_request(request)
    remind_at = datetime.fromisoformat(payload.get("remind_at"))
    r = Reminder(user_id=user_id, related_type=payload.get("related_type"), related_id=int(payload.get("related_id")), remind_at=remind_at)
    session.add(r)
    session.commit()
    session.refresh(r)
    return {"ok": True, "reminder_id": r.id}

@router.get("")
def list_reminders(request: Request, session: Session = Depends(get_session)):
    user_id = get_user_id_from_request(request)
    stmt = select(Reminder).where(Reminder.user_id==user_id)
    recs = session.exec(stmt).all()
    return recs
