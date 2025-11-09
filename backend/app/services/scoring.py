# app/services/scoring.py
"""
Business health scoring:
- profit_margin_trend (40%)
- current_month_profit / liquidity (30%)
- tax_due_ratio (20%)
- expense_volatility (10%)
All normalized to 0-100
"""
from typing import List, Dict
import numpy as np

def compute_health_score(monthly_income: List[float], monthly_expense: List[float], tax_due: float) -> int:
    # ensure same length
    n = min(len(monthly_income), len(monthly_expense))
    if n == 0:
        return 20  # minimal data
    income = np.array(monthly_income[-n:])
    expense = np.array(monthly_expense[-n:])
    profit = income - expense
    # profit margin trend: slope of profit over time normalized
    t = np.arange(len(profit)).reshape(-1,1)
    # simple linear slope
    try:
        coef = np.polyfit(np.arange(len(profit)), profit, 1)[0]
    except:
        coef = 0.0
    # normalize coef to score between 0-100 (heuristic)
    profit_trend_score = min(100, max(0, 50 + coef))  # heuristic
    # current month liquidity (current profit relative to average)
    current_profit = float(profit[-1])
    avg_profit = float(np.mean(profit)) if np.mean(profit)!=0 else 1.0
    liquidity_score = min(100, max(0, 50 + (current_profit - avg_profit) / (abs(avg_profit)+1) * 50))
    # tax due ratio (lower due -> higher score)
    tax_ratio = tax_due / (income.sum() + 1)
    tax_score = min(100, max(0, 100 - tax_ratio*100))
    # expense volatility (lower vol -> higher score)
    vol = float(np.std(expense))
    vol_score = min(100, max(0, 100 - vol/ (np.mean(expense)+1) * 50))
    # weighted
    total = 0.4*profit_trend_score + 0.3*liquidity_score + 0.2*tax_score + 0.1*vol_score
    return int(round(total))
