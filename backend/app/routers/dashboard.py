# app/routers/dashboard.py
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models.transaction import Transaction
from ..services.forecast import train_monthly_forecast
from ..services.scoring import compute_health_score
from collections import defaultdict
from datetime import datetime, date, timedelta

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

def get_current_user_id_from_request(request: Request):
    auth = request.headers.get("authorization")
    if not auth:
        raise HTTPException(status_code=401, detail="Missing auth")
    token = auth.split(" ")[1]
    from ..utils.security import decode_token
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return int(payload.get("sub"))

@router.get("/summary")
def summary(request: Request, session: Session = Depends(get_session)):
    user_id = get_current_user_id_from_request(request)
    # totals for current month and year
    today = date.today()
    start_month = date(today.year, today.month, 1)
    start_year = date(today.year, 1, 1)
    stmt = select(Transaction).where(Transaction.user_id==user_id)
    txs = session.exec(stmt).all()
    income_total = 0.0
    expense_total = 0.0
    # monthly aggregates for last 12 months
    monthly = defaultdict(float)
    for tx in txs:
        key = datetime(tx.date.year, tx.date.month, 1)
        if tx.type.upper() == "INCOME":
            income_total += tx.amount
            monthly[key] += tx.amount
        else:
            expense_total += tx.amount
            monthly[key] -= tx.amount
    profit_total = income_total - expense_total
    # prepare time series last 12 months
    series = []
    last12 = []
    for i in range(11, -1, -1):
        m = (today.replace(day=1) - timedelta(days=30*i)).replace(day=1)
        val = float(monthly.get(m, 0.0))
        series.append({"date": m.strftime("%Y-%m-%d"), "value": val})
        last12.append({"year": m.year, "month": m.month, "value": val})
    # forecasting
    forecast = train_monthly_forecast(user_id, last12)
    # health score: use monthly incomes and expenses arrays
    monthly_income = [max(0, x) for x in [d["value"] for d in last12]]
    monthly_expense = [max(0, -x) for x in [d["value"] for d in last12]]
    # tax due simple sum of unpaid tax records
    from ..models.tax import TaxRecord
    stmt_tax = select(TaxRecord).where(TaxRecord.user_id==user_id, TaxRecord.paid_boolean==False)
    unpaid = session.exec(stmt_tax).all()
    tax_due = sum([t.payable for t in unpaid]) if unpaid else 0.0
    score = compute_health_score(monthly_income, monthly_expense, tax_due)
    return {
        "totals": {"income_total": round(income_total,2), "expense_total": round(expense_total,2), "profit_total": round(profit_total,2)},
        "time_series": series,
        "ai_forecast": forecast,
        "business_health_score": score
    }

@router.get("/category-breakdown")
def category_breakdown(request: Request, session: Session = Depends(get_session)):
    user_id = get_current_user_id_from_request(request)
    stmt = select(Transaction).where(Transaction.user_id==user_id)
    txs = session.exec(stmt).all()
    cat = {}
    total_income = sum([t.amount for t in txs if t.type.upper()=="INCOME"])
    totals = {}
    for t in txs:
        totals.setdefault(t.category, 0.0)
        totals[t.category] += t.amount if t.type.upper()=="INCOME" else -t.amount
    breakdown = [{"category": k, "amount": v, "percentage": round((v/total_income*100) if total_income else 0,2)} for k,v in totals.items()]
    return {"breakdown": breakdown}
