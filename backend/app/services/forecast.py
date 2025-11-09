# app/services/forecast.py
"""
Simple forecasting service using sklearn LinearRegression on monthly aggregates.
Saves minimal artifacts in-memory (or can persist per-user if needed).
Fallback: return None if <6 months data.
"""
from typing import List, Dict, Optional, Tuple
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle
from datetime import datetime

# minimal in-memory store for demo; for production persist to DB or files
_model_store = {}

def train_monthly_forecast(user_id: int, monthly_series: List[Dict]) -> Optional[dict]:
    """
    monthly_series: list of {"year":2024,"month":1,"value":1000}
    returns forecast for next 3 months and simple confidence estimate
    """
    if len(monthly_series) < 6:
        return None
    # create DataFrame sorted by year,month
    df = pd.DataFrame(monthly_series)
    df['date'] = pd.to_datetime(df.assign(day=1)[['year','month','day']])
    df = df.sort_values('date')
    df['t'] = np.arange(len(df))  # time index
    X = df[['t']].values
    y = df['value'].values
    model = LinearRegression()
    model.fit(X, y)
    # forecast next 3 points
    last_t = int(df['t'].iloc[-1])
    future_t = np.array([[last_t + i] for i in range(1,4)])
    preds = model.predict(future_t).tolist()
    # simple confidence: 1 - (std of residuals / mean)
    residuals = y - model.predict(X)
    std = float(np.std(residuals))
    mean = float(np.mean(np.abs(y))) if len(y)>0 and np.mean(np.abs(y))>0 else 1.0
    confidence = max(0.0, min(1.0, 1 - std/mean))
    # store artifact
    _model_store[user_id] = pickle.dumps(model)
    return {
        "predictions": [{"month_offset": i, "value": float(preds[i-1])} for i in range(1,4)],
        "confidence": confidence,
        "trained_at": datetime.utcnow().isoformat()
    }

def load_model(user_id: int):
    raw = _model_store.get(user_id)
    if not raw:
        return None
    try:
        return pickle.loads(raw)
    except:
        return None
