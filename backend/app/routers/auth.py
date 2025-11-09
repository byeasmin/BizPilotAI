# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from ..schemas.auth import SignupSchema, Token
from ..models.user import User
from ..database import get_session
from ..utils.security import hash_password, verify_password, create_access_token
from datetime import timedelta
from ..core import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=Token)
def signup(payload: SignupSchema, session: Session = Depends(get_session)):
    stmt = select(User).where(User.email==payload.email)
    existing = session.exec(stmt).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    user = User(name=payload.name, email=payload.email, password_hash=hash_password(payload.password))
    session.add(user)
    session.commit()
    session.refresh(user)
    token = create_access_token(subject=str(user.id), expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(payload: SignupSchema, session: Session = Depends(get_session)):
    stmt = select(User).where(User.email==payload.email)
    user = session.exec(stmt).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(subject=str(user.id), expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": token, "token_type": "bearer"}
