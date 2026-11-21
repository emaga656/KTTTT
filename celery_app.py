import os

from celery import Celery

broker_url = os.getenv("CELERY_BROKER", "redis://localhost:6379/0")

celery_app = Celery(
    "tasks",
    broker=broker_url,
    backend=broker_url,
)


@celery_app.task
def background_task(message: str):
    print(f"Задача выполнена: {message}", flush=True)
    return message
