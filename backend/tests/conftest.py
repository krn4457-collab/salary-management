"""Shared in-memory DB fixture."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models import Employee


@pytest.fixture()
def db_session():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)
    s = TestingSession()
    try:
        yield s
    finally:
        s.close()


@pytest.fixture()
def client(db_session):
    def override():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = override
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def sample(db_session):
    from datetime import date
    rows = [
        Employee(first_name="A", last_name="Alpha", email="a@acme.example.com", country="India",
                 department="Engineering", level="L3", base_salary=800000, currency="INR",
                 salary_usd=9600, join_date=date(2020, 1, 15)),
        Employee(first_name="B", last_name="Beta", email="b@acme.example.com", country="USA",
                 department="Finance", level="L4", base_salary=150000, currency="USD",
                 salary_usd=150000, join_date=date(2019, 6, 1)),
        Employee(first_name="C", last_name="Gamma", email="c@acme.example.com", country="India",
                 department="Engineering", level="L2", base_salary=500000, currency="INR",
                 salary_usd=6000, join_date=date(2022, 3, 10)),
    ]
    db_session.add_all(rows)
    db_session.commit()
    return rows
