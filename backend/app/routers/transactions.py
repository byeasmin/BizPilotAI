# app/routers/transactions.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from sqlmodel import Session, select
from ..schemas.transaction import TransactionCreate, TransactionRead
from ..models.transaction import Transaction
from ..database import get_session
from ..utils.security import decode_token
from fastapi import Request

router = APIRouter(prefix="/transactions", tags=["transactions"])

def get_current_user_id(request: Request):
    auth = request.headers.get("authorization")
    if not auth:
        raise HTTPException(status_code=401, detail="Missing auth")
    token = auth.split(" ")[1]
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return int(payload.get("sub"))

@router.post("", response_model=TransactionRead)
def create_transaction(payload: TransactionCreate, session: Session = Depends(get_session), request: Request = None):
    user_id = get_current_user_id(request)
    tx = Transaction(user_id=user_id, type=payload.type.upper(), amount=payload.amount, date=payload.date, category=payload.category, description=payload.description, currency=payload.currency)
    session.add(tx)
    session.commit()
    session.refresh(tx)
    return tx

@router.get("", response_model=List[TransactionRead])
def list_transactions(page: int = 1, page_size: int = 50, date_from: str = Query(None), date_to: str = Query(None), type: str = Query(None), category: str = Query(None), session: Session = Depends(get_session), request: Request = None):
    user_id = get_current_user_id(request)
    stmt = select(Transaction).where(Transaction.user_id==user_id)
    if type:
        stmt = stmt.where(Transaction.type==type.upper())
    if category:
        stmt = stmt.where(Transaction.category==category)
    if date_from:
        stmt = stmt.where(Transaction.date >= date_from)
    if date_to:
        stmt = stmt.where(Transaction.date <= date_to)
    stmt = stmt.order_by(Transaction.date.desc()).offset((page-1)*page_size).limit(page_size)
    results = session.exec(stmt).all()
    return results

@router.get("/{id}", response_model=TransactionRead)
def get_transaction(id: int, session: Session = Depends(get_session), request: Request = None):
    user_id = get_current_user_id(request)
    stmt = select(Transaction).where(Transaction.id==id, Transaction.user_id==user_id)
    tx = session.exec(stmt).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Not found")
    return tx

@router.put("/{id}", response_model=TransactionRead)
def update_transaction(id: int, payload: TransactionCreate, session: Session = Depends(get_session), request: Request = None):
    user_id = get_current_user_id(request)
    stmt = select(Transaction).where(Transaction.id==id, Transaction.user_id==user_id)
    tx = session.exec(stmt).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Not found")
    tx.type = payload.type.upper()
    tx.amount = payload.amount
    tx.date = payload.date
    tx.category = payload.category
    tx.description = payload.description
    tx.currency = payload.currency
    session.add(tx)
    session.commit()
    session.refresh(tx)
    return tx

@router.delete("/{id}")
def delete_transaction(id: int, session: Session = Depends(get_session), request: Request = None):
    user_id = get_current_user_id(request)
    stmt = select(Transaction).where(Transaction.id==id, Transaction.user_id==user_id)
    tx = session.exec(stmt).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Not found")
    session.delete(tx)
    session.commit()
    return {"ok": True}
