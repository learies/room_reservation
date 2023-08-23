from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.meeting_room import meeting_room_crud
from app.models import MeetingRoom


async def check_name_duplicate(
    room_name: str,
    session: AsyncSession,
) -> None:
    """Проверяет, наличие переговорки с таким же именем.

    Args:
        room_name (str): Название переговорки.
        session (AsyncSession): Сессия базы данных.

    Raises:
        HTTPException: Если переговорка с таким именем уже существует.

    Returns:
        None
    """
    room_id = await meeting_room_crud.get_room_id_by_name(
        room_name,
        session,
    )
    if room_id:
        raise HTTPException(
            status_code=422,
            detail="Переговорка с таким именем уже существует!",
        )


async def check_meeting_room_exists(
    meeting_room_id: int,
    session: AsyncSession,
) -> MeetingRoom:
    """Проверяет, наличие переговорки по Идентификатору id.

    Args:
        meeting_room_id (int): Идентификатор переговорки.
        session (AsyncSession): Сессия базы данных.

    Raises:
        HTTPException: Если переговорка не найдена или удалена.

    Returns:
        MeetingRoom: Объект переговорки.
    """

    meeting_room = await meeting_room_crud.get_by_id(
        meeting_room_id,
        session,
    )
    if not meeting_room or not meeting_room.is_active:
        raise HTTPException(
            status_code=404,
            detail="Переговорка не найдена!",
        )
    return meeting_room
