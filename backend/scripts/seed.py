"""Deterministic seed of 10,000 employees. Idempotent. Run: python scripts/seed.py"""

import random
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import delete
from app.database import Base, SessionLocal, engine
from app.models import EXCHANGE_TO_USD, Employee

random.seed(42)

FIRST = ["Aarav", "Priya", "John", "Maria", "Chen", "Fatima", "James", "Sofia", "Ravi", "Emma",
         "Liam", "Olivia", "Noah", "Aisha", "Diego", "Yuki", "Omar", "Anna", "Rahul", "Grace",
         "Michael", "Sarah", "David", "Laura", "Kevin", "Nina", "Arjun", "Meera", "Tom", "Elena"]
LAST = ["Sharma", "Patel", "Smith", "Garcia", "Wang", "Khan", "Brown", "Rossi", "Iyer", "Johnson",
        "Lee", "Muller", "Silva", "Nguyen", "Kumar", "Tanaka", "Ali", "Novak", "Gupta", "Wilson",
        "Taylor", "Anderson", "Thomas", "Moore", "Martin", "Singh", "Das", "Kaur", "Clark", "Lewis"]

COUNTRIES = [  # (country, currency, weight)
    ("India", "INR", 30), ("USA", "USD", 22), ("UK", "GBP", 8), ("Germany", "EUR", 8),
    ("Singapore", "SGD", 6), ("Australia", "AUD", 6), ("Canada", "CAD", 5), ("UAE", "AED", 5),
    ("Brazil", "BRL", 4), ("Japan", "JPY", 3), ("Nigeria", "NGN", 2), ("France", "EUR", 1),
]
DEPARTMENTS = ["Engineering", "HR", "Finance", "Sales", "Marketing", "Support", "Data", "Operations"]
LEVELS = ["L1", "L2", "L3", "L4", "L5"]
# USD base bands per level
BANDS = {"L1": (30000, 55000), "L2": (50000, 85000), "L3": (80000, 130000), "L4": (120000, 180000), "L5": (170000, 260000)}

LEVEL_W = [30, 30, 22, 12, 6]


def pick_weighted(items, weights):
    return random.choices(items, weights=weights, k=1)[0]


def main(n: int = 10000):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    db.execute(delete(Employee))
    db.commit()

    country_names = [c[0] for c in COUNTRIES]
    country_w = [c[2] for c in COUNTRIES]
    country_ccy = {c[0]: c[1] for c in COUNTRIES}

    batch = []
    for i in range(1, n + 1):
        fn = random.choice(FIRST)
        ln = random.choice(LAST)
        country = pick_weighted(country_names, country_w)
        ccy = country_ccy[country]
        dept = random.choice(DEPARTMENTS)
        level = pick_weighted(LEVELS, LEVEL_W)
        lo, hi = BANDS[level]
        salary_usd = round(random.uniform(lo, hi), 2)
        rate = EXCHANGE_TO_USD.get(ccy, 1.0)
        base_local = round(salary_usd / rate, 2)
        year = random.randint(2016, 2024)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        batch.append(Employee(
            first_name=fn, last_name=ln,
            email=f"{fn.lower()}.{ln.lower()}.{i}@acme.example.com",
            country=country, department=dept, level=level,
            base_salary=base_local, currency=ccy, salary_usd=salary_usd,
            join_date=date(year, month, day),
        ))
        if len(batch) >= 1000:
            db.add_all(batch)
            db.commit()
            batch.clear()
    if batch:
        db.add_all(batch)
        db.commit()
    count = n
    print(f"Seeded {count} employees.")
    db.close()


if __name__ == "__main__":
    arg = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    main(arg)
