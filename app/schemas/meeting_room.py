from pydantic import BaseModel, Field, field_validator


class MeetingRoomBase(BaseModel):
    """Базовая схема переговорки.

    Args:
        name (None or str): Название переговорки.
        description (None or str): Описание переговорки.
    """

    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, min_length=1, max_length=500)


class MeetingRoomCreate(MeetingRoomBase):
    """Схема создания переговорки.

    Args:
        name (str): Название переговорки, обязательное поле.
    """

    name: str = Field(..., min_length=1, max_length=100)


class MeetingRoomUpdate(MeetingRoomBase):
    """Схема обновления переговорки.

    Args:
        name (str): Название переговорки, не может быть пустым при обновлении.
    """

    @field_validator("name")
    def name_cannot_be_null(cls, value: str) -> str:
        if value is None:
            raise ValueError("Имя переговорки не может быть пустым!")
        return value


class MeetingRoomResponse(MeetingRoomBase):
    """Схема ответа с информацией о переговорки.

    Args:
        id (int): Идентификатор переговорки.
    """

    id: int

    class Config:
        from_attributes = True
