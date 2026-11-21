import os
import psycopg2
import redis
from fastapi import FastAPI, HTTPException

app = FastAPI(title="KT: Контейнеризация и автоматический деплой")


def check_database() -> bool:
    connection = psycopg2.connect(os.environ["DATABASE_URL"], connect_timeout=3)
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            return cursor.fetchone()[0] == 1
    finally:
        connection.close()


def check_redis() -> bool:
    client = redis.Redis.from_url(
        os.environ["CELERY_BROKER"],
        socket_connect_timeout=3,
        socket_timeout=3,
    )
    return bool(client.ping())

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/app_db")
REDIS_URL = os.getenv("REDIS_URL")



@app.get("/")
def root():
    return {"message": "Hello from KT!", "status": "running"}


@app.get("/health")
def health_check():
    status = {"app": "ok", "db": "error", "redis": "error"}
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.close()
        status["db"] = "connected"
    except Exception as e:
        status["db_error"] = str(e)

    try:
        r = redis.Redis.from_url(REDIS_URL, socket_connect_timeout=2)
        if r.ping():
            status["redis"] = "connected"
    except Exception as e:
        status["redis_error"] = str(e)

    if status["db"] != "connected" or status["redis"] != "connected":
        raise HTTPException(status_code=503, detail=status)
        
    return status
