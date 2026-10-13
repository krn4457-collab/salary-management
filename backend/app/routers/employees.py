"""Employee CRUD + list with search/filter/sort/pagination."""

from typing import Literal, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import asc, desc, or_, select, func
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Employee, to_usd
from ..schemas import EmployeeCreate, EmployeeOut, FilterMeta, PaginatedEmployees, SalaryUpdate

router = APIRouter(prefix="/api/employees", tags=["employees"])

SORTABLE = {"salary_usd": Employee.salary_usd, "join_date": Employee.join_date, "last_name": Employee.last_name}


@router.get("", response_model=PaginatedEmployees)
def list_employees(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    country: Optional[str] = None,
    department: Optional[str] = None,
    level: Optional[str] = None,
    sort_by: Literal["salary_usd", "join_date", "last_name"] = "last_name",
    sort_dir: Literal["asc", "desc"] = "asc",
    db: Session = Depends(get_db),
):
    q = select(Employee)
    count_q = select(func.count()).select_from(Employee)
    filters = []
    if search:
        like = f"%{search}%"
        filters.append(or_(Employee.first_name.ilike(like), Employee.last_name.ilike(like), Employee.email.ilike(like)))
    if country:
        filters.append(Employee.country == country)
    if department:
        filters.append(Employee.department == department)
    if level:
        filters.append(Employee.level == level)
    for f in filters:
        q = q.where(f)
        count_q = count_q.where(f)

    total = db.execute(count_q).scalar_one()
    col = SORTABLE[sort_by]
    q = q.order_by(asc(col) if sort_dir == "asc" else desc(col))
    q = q.offset((page - 1) * page_size).limit(page_size)
    items = db.execute(q).scalars().all()
    return {"total": total, "page": page, "page_size": page_size, "items": items}


@router.get("/meta/filters", response_model=FilterMeta)
def filter_meta(db: Session = Depends(get_db)):
    def distinct(col):
        return [r[0] for r in db.execute(select(col).distinct().order_by(col)).all()]
    return {
        "countries": distinct(Employee.country),
        "departments": distinct(Employee.department),
        "levels": distinct(Employee.level),
        "currencies": distinct(Employee.currency),
    }


@router.get("/{emp_id}", response_model=EmployeeOut)
def get_employee(emp_id: int, db: Session = Depends(get_db)):
    emp = db.get(Employee, emp_id)
    if not emp:
        raise HTTPException(404, "Employee not found")
    return emp


@router.post("", response_model=EmployeeOut, status_code=201)
def create_employee(payload: EmployeeCreate, db: Session = Depends(get_db)):
    if db.execute(select(Employee).where(Employee.email == payload.email)).scalar_one_or_none():
        raise HTTPException(409, "Email already exists")
    emp = Employee(**payload.model_dump(), salary_usd=to_usd(payload.base_salary, payload.currency))
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp


@router.patch("/{emp_id}", response_model=EmployeeOut)
def update_salary(emp_id: int, payload: SalaryUpdate, db: Session = Depends(get_db)):
    emp = db.get(Employee, emp_id)
    if not emp:
        raise HTTPException(404, "Employee not found")
    emp.base_salary = payload.base_salary
    emp.salary_usd = to_usd(payload.base_salary, emp.currency)
    db.commit()
    db.refresh(emp)
    return emp


@router.delete("/{emp_id}", status_code=204)
def delete_employee(emp_id: int, db: Session = Depends(get_db)):
    emp = db.get(Employee, emp_id)
    if not emp:
        raise HTTPException(404, "Employee not found")
    db.delete(emp)
    db.commit()
    return None
