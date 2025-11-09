# app/utils/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from sqlmodel import Session, select
from ..database import engine
from ..models.reminder import Reminder

_scheduler = BackgroundScheduler()

def check_reminders():
    with Session(engine) as session:
        now = datetime.utcnow()
        stmt = select(Reminder).where(Reminder.sent_boolean==False, Reminder.remind_at <= now)
        reminders = session.exec(stmt).all()
        for r in reminders:
            # for demo, "send" by logging to console
            print(f"[Reminder] sending reminder id={r.id} for user={r.user_id} related={r.related_type}/{r.related_id}")
            r.sent_boolean = True
            session.add(r)
        session.commit()

def start_scheduler(interval_seconds: int = 30):
    _scheduler.add_job(check_reminders, 'interval', seconds=interval_seconds, id="reminder_check", replace_existing=True)
    _scheduler.start()
