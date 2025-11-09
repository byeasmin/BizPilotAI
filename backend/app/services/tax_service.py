# app/services/tax_service.py
from datetime import date, datetime, timedelta
from typing import Tuple, Dict
from ..models.tax import TaxConfig, TaxRecord
from sqlmodel import Session, select
from ..database import engine

def compute_tax_for_period(user_id: int, year: int, month: int, taxable_amount: float, session: Session) -> Dict:
    # load tax config if exists
    stmt = select(TaxConfig).where(TaxConfig.user_id==user_id, TaxConfig.year==year)
    cfg = session.exec(stmt).first()
    if cfg:
        vat_rate = cfg.vat_rate
        tax_rate = cfg.tax_rate
    else:
        vat_rate = 0.15
        tax_rate = 0.0
    vat_amount = round(taxable_amount * vat_rate, 2)
    tax_amount = round(taxable_amount * tax_rate, 2)
    payable = round(taxable_amount + vat_amount + tax_amount, 2)
    # due date: 15th next month (simple rule)
    due_date = None
    try:
        if month < 12:
            due_date = date(year, month+1, 15)
        else:
            due_date = date(year+1, 1, 15)
    except Exception:
        due_date = date.today() + timedelta(days=30)
    # create TaxRecord
    record = TaxRecord(
        user_id=user_id,
        year=year,
        month=month,
        taxable_amount=taxable_amount,
        vat_amount=vat_amount,
        tax_amount=tax_amount,
        payable=payable,
        due_date=due_date
    )
    session.add(record)
    session.commit()
    session.refresh(record)
    return {
        "taxable_amount": taxable_amount,
        "vat_amount": vat_amount,
        "tax_amount": tax_amount,
        "payable": payable,
        "due_date": due_date.isoformat()
    }
