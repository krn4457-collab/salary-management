"""ACME Salary Management API."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from . import models  # noqa: F401  (register tables)
from .routers import employees

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ACME Salary Management API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employees.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
