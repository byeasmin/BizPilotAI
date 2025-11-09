# app/models/reminder.py
from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

class Reminder(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    related_type: str
    related_id: int
    remind_at: datetime
    sent_boolean: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
