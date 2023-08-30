import asyncio
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.config import settings

try:
    from app.main import app
except (NameError, ImportError):
    raise AssertionError(
        "Не обнаружен объект приложения `app`."
        "Проверьте и поправьте: он должен быть доступен в модуле `app.main`.",
    )

try:
    from app.core.db import Base, get_async_session
except (NameError, ImportError):
    raise AssertionError(
        "Не обнаружены объекты `Base, get_async_session`. "
        "Проверьте и поправьте: они должны быть доступны в модуле `app.core.db`.",
    )

SQLALCHEMY_DATABASE_URL = settings.database_url_test
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, poolclass=NullPool)
TestingSessionLocal = async_sessionmaker(
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    bind=engine,
)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as override_async_session:
        yield override_async_session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope="session")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def client():
    with TestClient(app) as client:
        yield client
