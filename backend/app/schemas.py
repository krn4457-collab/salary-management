"""Pydantic schemas."""

from datetime import date, datetime
from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class EmployeeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    email: str
    country: str
    department: str
    level: str
    base_salary: float
    currency: str
    salary_usd: float
    join_date: date
    updated_at: datetime


class EmployeeCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    email: str
    country: str
    department: str
    level: str
    base_salary: float = Field(gt=0, lt=1_000_000)
    currency: str = "USD"
    join_date: date


class SalaryUpdate(BaseModel):
    base_salary: float = Field(gt=0, lt=1_000_000)


class PaginatedEmployees(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[EmployeeOut]


class FilterMeta(BaseModel):
    countries: List[str]
    departments: List[str]
    levels: List[str]
    currencies: List[str]
