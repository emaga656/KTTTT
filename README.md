# FastAPI + Docker Compose

Учебный проект: FastAPI, PostgreSQL, Redis и Celery Worker.

## Запуск

1. Установите и запустите Docker Desktop.
2. Откройте терминал в корневой папке проекта.
3. Выполните:

```bash
docker compose up --build
```

После запуска откройте:

- http://localhost:8000 — главная страница;
- http://localhost:8000/docs — Swagger;
- http://localhost:8000/health — проверка приложения;
- http://localhost:8000/health/db — проверка PostgreSQL.

## Проверка Celery

В Swagger выполните `POST /tasks`. Затем в другом терминале запустите:

```bash
docker compose logs -f celery_worker
```

В логах воркера должно появиться сообщение о выполнении задачи.

## Полезные команды

```bash
docker compose ps
docker compose logs app
docker compose logs celery_worker
docker compose down
```

`docker compose down -v` удаляет также том PostgreSQL и сохранённые данные.

## Переменные окружения

`.env.docker` используется контейнерами. Внутри Docker-сети PostgreSQL доступен по имени `db`, Redis — по имени `redis`. Поэтому в этих переменных нельзя указывать `localhost`.

`.env` оставлен для локального запуска приложения вне Docker.

## Автоматические тесты

GitHub Actions запускает `pytest` при `push` и `pull_request` в ветку `main`.
Workflow находится в `.github/workflows/tests.yml`.

Для сдачи задания дополнительно загрузите проект в GitHub, отправьте изменения в ветку `main`, а затем разверните приложение на Railway или VPS. После реального деплоя впишите публичный адрес приложения сюда. Не указывайте localhost в качестве публичного адреса.

**Публичный адрес:** добавить после деплоя.
