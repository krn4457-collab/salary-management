"""Payroll analytics — answers 'how do we pay people?'."""

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Employee

router = APIRouter(prefix="/api/stats", tags=["stats"])


@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    total, headcount, avg = db.execute(
        select(func.coalesce(func.sum(Employee.salary_usd), 0), func.count(), func.coalesce(func.avg(Employee.salary_usd), 0))
    ).one()
    median = db.execute(
        select(Employee.salary_usd).order_by(Employee.salary_usd).offset(headcount // 2).limit(1)
    ).scalar() if headcount else 0
    return {
        "headcount": headcount,
        "total_payroll_usd": round(total or 0, 2),
        "avg_salary_usd": round(avg or 0, 2),
        "median_salary_usd": round(median or 0, 2),
    }


@router.get("/by-department")
def by_department(db: Session = Depends(get_db)):
    rows = db.execute(
        select(Employee.department, func.count(), func.avg(Employee.salary_usd), func.sum(Employee.salary_usd))
        .group_by(Employee.department).order_by(Employee.department)
    ).all()
    return [{"department": d, "headcount": c, "avg_usd": round(a, 2), "total_usd": round(t, 2)} for d, c, a, t in rows]


@router.get("/by-country")
def by_country(db: Session = Depends(get_db)):
    rows = db.execute(
        select(Employee.country, func.count(), func.avg(Employee.salary_usd))
        .group_by(Employee.country).order_by(func.avg(Employee.salary_usd).desc())
    ).all()
    return [{"country": c, "headcount": n, "avg_usd": round(a, 2)} for c, n, a in rows]


@router.get("/by-level")
def by_level(db: Session = Depends(get_db)):
    rows = db.execute(
        select(Employee.level, func.count(), func.avg(Employee.salary_usd))
        .group_by(Employee.level)
    ).all()
    order = {"L1": 0, "L2": 1, "L3": 2, "L4": 3, "L5": 4}
    out = [{"level": lv, "headcount": n, "avg_usd": round(a, 2)} for lv, n, a in rows]
    return sorted(out, key=lambda r: order.get(r["level"], 99))


@router.get("/top-earners")
def top_earners(limit: int = 10, db: Session = Depends(get_db)):
    limit = max(1, min(limit, 50))
    rows = db.execute(select(Employee).order_by(Employee.salary_usd.desc()).limit(limit)).scalars().all()
    return [
        {"id": e.id, "name": f"{e.first_name} {e.last_name}", "department": e.department,
         "country": e.country, "salary_usd": e.salary_usd}
        for e in rows
    ]
