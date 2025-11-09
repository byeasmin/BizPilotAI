# app/models/tax.py
from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime, date
from typing import Dict, Any
import json

class TaxConfig(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    year: int
    vat_rate: float = 0.15
    tax_rate: float = 0.0
    thresholds_json: Optional[str] = Field(default='{}')

    def thresholds(self) -> Dict[str, Any]:
        try:
            return json.loads(self.thresholds_json or "{}")
        except:
            return {}

class TaxRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    year: int
    month: int
    taxable_amount: float
    vat_amount: float
    tax_amount: float
    payable: float
    due_date: Optional[date] = None
    paid_boolean: bool = False
    generated_at: datetime = Field(default_factory=datetime.utcnow)
