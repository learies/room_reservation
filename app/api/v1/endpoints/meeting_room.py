from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.validators import (
    check_meeting_room_exists,
    check_name_duplicate,
)
from app.core.db import get_async_session
from app.crud import meeting_room_crud
from app.models.meeting_room import MeetingRoom
from app.schemas.meeting_room import (
    MeetingRoomCreate,
    MeetingRoomResponse,
    MeetingRoomUpdate,
)

router = APIRouter()


@router.get(
    "/",
    response_model=list[MeetingRoomResponse],
    response_model_exclude_none=True,
)
async def get_all_meeting_rooms(
    session: AsyncSession = Depends(get_async_session),
) -> list[MeetingRoom]:
    """Получить список переговорок.

    Args:
        session (AsyncSession): Сессия базы данных.

    Returns:
        list[MeetingRoom]: Список переговорок.
    """
    all_rooms = await meeting_room_crud.get_all_active(session)
    return all_rooms


@router.get(
    "/{meeting_room_id}",
    response_model=MeetingRoomResponse,
    response_model_exclude_none=True,
)
async def get_meeting_room_by_id(
    meeting_room_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> MeetingRoom:
    """Получить переговорку по идентификатору id.

    Args:
        meeting_room_id (int): Идентификатор переговорки.
        session (AsyncSession): Сессия базы данных.

    Raises:
        HTTPException: Если переговорка не найдена.

    Returns:
        MeetingRoom: Объект переговорки.
    """
    meeting_room = await check_meeting_room_exists(
        meeting_room_id,
        session,
    )
    return meeting_room


@router.post(
    "/",
    response_model=MeetingRoomResponse,
    response_model_exclude_none=True,
)
async def create_new_meeting_room(
    meeting_room: MeetingRoomCreate,
    session: AsyncSession = Depends(get_async_session),
) -> MeetingRoom:
    """Создать переговорку или восстановить удалённую.

    Args:
        meeting_room (MeetingRoomCreate): Данные по переговорке.
        session (AsyncSession): Сессия базы данных.

    Raises:
        HTTPException: Если переговорка с таким именем уже существует.

    Returns:
        MeetingRoom: Объект переговорки.
    """
    deleted_meeting_room = await check_name_duplicate(
        meeting_room.name,
        session,
    )

    if deleted_meeting_room:
        restore_room = await meeting_room_crud.restore(
            deleted_meeting_room,
            meeting_room,
            session,
        )
        return restore_room

    new_room = await meeting_room_crud.create(
        meeting_room,
        session,
    )
    return new_room


@router.patch(
    "/{meeting_room_id}",
    response_model=MeetingRoomResponse,
    response_model_exclude_none=True,
)
async def partially_update_meeting_room(
    meeting_room_id: int,
    obj_in: MeetingRoomUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> MeetingRoom:
    """Обновить информацию по переговорке.

    Args:
        meeting_room_id (int): Идентификатор переговорки.
        obj_in (MeetingRoomUpdate): Данные для обновления переговорки.
        session (AsyncSession): Сессия базы данных.

    Raises:
        HTTPException: Если переговорка не найдена или удалена.

    Returns:
        MeetingRoom: Объект обновленной переговорки.
    """
    meeting_room = await check_meeting_room_exists(
        meeting_room_id,
        session,
    )

    # Позволяет изменять информацию переговорки
    # без необходимости менять название.
    if obj_in.name != meeting_room.name:
        await check_name_duplicate(obj_in.name, session)

    meeting_room = await meeting_room_crud.update(
        meeting_room,
        obj_in,
        session,
    )
    return meeting_room


@router.delete(
    "/{meeting_room_id}",
    response_model=MeetingRoomResponse,
    response_model_exclude_none=True,
)
async def remove_meeting_room(
    meeting_room_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> MeetingRoom:
    """Удалить переговорку.

    Args:
        meeting_room_id (int): Идентификатор переговорки.
        session (AsyncSession): Сессия базы данных.

    Raises:
        HTTPException: Если переговорка не найдена в базе данных.

    Returns:
        MeetingRoom: Объект удаленной переговорки.
    """
    meeting_room = await check_meeting_room_exists(meeting_room_id, session)
    meeting_room = await meeting_room_crud.remove(meeting_room, session)
    return meeting_room
