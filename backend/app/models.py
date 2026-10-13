"""Employee ORM model + currency normalization."""

from datetime import date, datetime
from sqlalchemy import Date, DateTime, Float, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base

# Static FX to USD for comparison dashboard (documented approximation).
EXCHANGE_TO_USD = {
    "USD": 1.0,
    "EUR": 1.08,
    "GBP": 1.27,
    "INR": 0.012,
    "SGD": 0.74,
    "AUD": 0.66,
    "CAD": 0.73,
    "AED": 0.272,
    "BRL": 0.20,
    "JPY": 0.0067,
    "NGN": 0.00065,
    "DE": 1.08,  # placeholder guard, unused
}


def to_usd(amount: float, currency: str) -> float:
    return round(amount * EXCHANGE_TO_USD.get(currency, 1.0), 2)


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)
    country: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    department: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    level: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    base_salary: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="USD")
    salary_usd: Mapped[float] = mapped_column(Float, nullable=False, index=True)
    join_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )
