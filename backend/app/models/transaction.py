# app/models/transaction.py
from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import date

class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    type: str  # "INCOME" or "EXPENSE"
    amount: float
    currency: str = "BDT"
    date: date
    category: str
    description: Optional[str] = None
