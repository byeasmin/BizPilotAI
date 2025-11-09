# seed_demo.py
import random
from datetime import date, timedelta
from sqlmodel import Session
from app.database import engine
from app.models.user import User
from app.models.transaction import Transaction
from app.utils.security import hash_password
from app.create_db import create_db_and_tables

def seed():
    create_db_and_tables()
    with Session(engine) as session:
        # create demo user
        user = User(name="Demo User", email="demo@example.com", password_hash=hash_password("password"))
        session.add(user)
        session.commit()
        session.refresh(user)
        # create 12 months of transactions
        today = date.today()
        for i in range(12):
            d = (today.replace(day=1) - timedelta(days=30*i)).replace(day=15)
            # incomes
            income_val = random.uniform(50000, 150000)
            tx_income = Transaction(user_id=user.id, type="INCOME", amount=round(income_val,2), date=d, category="sales", description="Monthly sales")
            session.add(tx_income)
            # expenses
            expense_val = random.uniform(30000, 80000)
            tx_exp = Transaction(user_id=user.id, type="EXPENSE", amount=round(expense_val,2), date=d, category="operations", description="Monthly ops")
            session.add(tx_exp)
        session.commit()
        print("Seeded demo user and transactions. email=demo@example.com password=password")

if __name__ == "__main__":
    seed()
