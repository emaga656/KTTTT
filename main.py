import os

import psycopg
from fastapi import FastAPI, HTTPException

from celery_app import background_task

app = FastAPI(title="FastAPI Docker Demo", version="1.0.0")


@app.get("/")
def home():
    return {"message": "FastAPI работает в Docker!"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/health/db")
def database_health():
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:secret@localhost:5432/appdb",
    )
    try:
        with psycopg.connect(database_url, connect_timeout=3) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
        return {"database": "connected"}
    except Exception:
        raise HTTPException(status_code=503, detail="Database unavailable")


@app.post("/tasks")
def create_task():
    task = background_task.delay("Hello from Docker!")
    return {"task_id": task.id, "status": "Задача отправлена"}
