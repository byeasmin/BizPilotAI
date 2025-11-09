# app/schemas/transaction.py
from pydantic import BaseModel
from datetime import date
from typing import Optional

class TransactionCreate(BaseModel):
    type: str
    amount: float
    date: date
    category: str
    description: Optional[str] = None
    currency: Optional[str] = "BDT"

class TransactionRead(TransactionCreate):
    id: int
    user_id: int
