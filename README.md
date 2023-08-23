# Бронирование переговорок

Api сервис для бронирования переговорных комнат

**Стек:**

- Python 3.11
- FastAPI
- Pydantic v2
- Alembic
- Docker
- Sqlalchemy v2
- PostgreSQL

**Создать виртуальное окружение**

```bash
...$ python3 -m venv .venv
```

```bash
...$ source .venv/bin/activate
```

**Установить зависимости**

```bash
(.venv) ...$ pip install -r requirements/prod.txt
```

**Создать файл .env**

```bash
(.venv) ...$ cp .env_template .env
```

**Запустить контейнер с PostgreSQL**

```bash
(.venv) ...$ docker-compose up -d
```

**Остановить контейнер с PostgreSQL**

```bash
(.venv) ...$ docker-compose down
```

**Создать миграции**

```bash
(.venv) ...$ alembic revision --autogenerate -m "First migration"
```

**Применение миграций**

```bash
(.venv) ...$ alembic upgrade head
```

**Отмена миграций**

```bash
(.venv) ...$ alembic downgrade base
```

**Запустить**

```bash
(.venv) ...$ uvicorn app.main:app --reload
```