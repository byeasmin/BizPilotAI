# app/routers/tax.py
from fastapi import APIRouter, Request, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..services.tax_service import compute_tax_for_period
from ..models.tax import TaxRecord
from ..models.transaction import Transaction
from datetime import datetime

router = APIRouter(prefix="/tax", tags=["tax"])

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

@router.post("/generate")
def generate_tax(payload: dict, request: Request, session: Session = Depends(get_session)):
    """
    payload: {"year":2024,"month":5}
    """
    user_id = get_user_id_from_request(request)
    year = int(payload.get("year"))
    month = int(payload.get("month"))
    # compute taxable_amount as sum of income for that month
    stmt = select(Transaction).where(Transaction.user_id==user_id)
    txs = session.exec(stmt).all()
    taxable = 0.0
    for tx in txs:
        if tx.date.year==year and tx.date.month==month and tx.type.upper()=="INCOME":
            taxable += tx.amount
    result = compute_tax_for_period(user_id, year, month, taxable, session)
    return {"status":"ok","summary": result}

@router.get("/{year}/{month}")
def get_tax(year: int, month: int, request: Request, session: Session = Depends(get_session)):
    user_id = get_user_id_from_request(request)
    stmt = select(TaxRecord).where(TaxRecord.user_id==user_id, TaxRecord.year==year, TaxRecord.month==month)
    rec = session.exec(stmt).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Not found")
    return rec

@router.get("/due")
def due(request: Request, days: int = 30, session: Session = Depends(get_session)):
    user_id = get_user_id_from_request(request)
    from datetime import date, timedelta
    today = date.today()
    end = today + timedelta(days=days)
    stmt = select(TaxRecord).where(TaxRecord.user_id==user_id, TaxRecord.paid_boolean==False, TaxRecord.due_date <= end)
    recs = session.exec(stmt).all()
    return {"due": recs}

@router.post("/mark-paid")
def mark_paid(payload: dict, request: Request, session: Session = Depends(get_session)):
    user_id = get_user_id_from_request(request)
    tr_id = int(payload.get("tax_id"))
    stmt = select(TaxRecord).where(TaxRecord.id==tr_id, TaxRecord.user_id==user_id)
    rec = session.exec(stmt).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Not found")
    rec.paid_boolean = True
    session.add(rec)
    session.commit()
    return {"ok": True}
