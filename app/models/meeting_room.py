from sqlalchemy import Boolean, Column, String, Text

from app.core.db import Base


class MeetingRoom(Base):
    """Модель переговорки.

    Args:
        name (str): Название переговорки уникальное и не более 100 символов.
        description (str): Описание переговорки.
        is_active (bool): Статус переговорки.
    """

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
