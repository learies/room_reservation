from datetime import datetime
from typing import AsyncGenerator

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base, declared_attr

from app.core.config import settings


def fresh_timestamp() -> datetime:
    """Временная метка."""
    return datetime.utcnow()


class PreBase:
    """Базовая модель.

    Args:
        id (int): Идентификатору id.
        created (datetime): Дата создания.
        updated (datetime): Дата обновления.
    """

    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=fresh_timestamp)
    updated = Column(DateTime, onupdate=fresh_timestamp)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.database_url)

AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as async_session:
        yield async_session
