from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_meeting_room_exists, check_name_duplicate
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.meeting_room import meeting_room_crud
from app.crud.reservation import reservation_crud
from app.models import MeetingRoom, Reservation
from app.schemas.meeting_room import (MeetingRoomCreate, MeetingRoomDB,
                                      MeetingRoomUpdate)
from app.schemas.reservation import ReservationDB

router = APIRouter()


@router.get(
    '/',
    response_model=list[MeetingRoomDB],
    response_model_exclude_none=True,
)
async def get_all_meeting_rooms(
    session: AsyncSession = Depends(get_async_session),
) -> list[MeetingRoom]:
    """Получить список всех переговорных комнат."""
    all_rooms = await meeting_room_crud.get_multi(session)
    return all_rooms


@router.post(
    '/',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_meeting_room(
    meeting_room: MeetingRoomCreate,
    session: AsyncSession = Depends(get_async_session),
) -> MeetingRoom:
    """Создаёт новую переговорную комнату. Только для суперюзера."""
    await check_name_duplicate(meeting_room.name, session)
    new_room = await meeting_room_crud.create(meeting_room, session)
    return new_room


@router.patch(
    '/{meeting_room_id}',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_meeting_room(
    meeting_room_id: int,
    obj_in: MeetingRoomUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> MeetingRoom:
    """Обновить информацию переговорной комнаты. Только для суперюзера."""
    meeting_room = await check_meeting_room_exists(meeting_room_id, session)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    meeting_room = await meeting_room_crud.update(
        meeting_room,
        obj_in,
        session,
    )
    return meeting_room


@router.delete(
    '/{meeting_room_id}',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_meeting_room(
    meeting_room_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> MeetingRoom:
    """Удалить переговорную комнату. Только для суперюзера."""
    meeting_room = await check_meeting_room_exists(meeting_room_id, session)
    meeting_room = await meeting_room_crud.remove(meeting_room, session)
    return meeting_room


@router.get(
    '/{meeting_room_id}/reservations',
    response_model=list[ReservationDB],
    response_model_exclude={'user_id'},
)
async def get_reservations_for_room(
    meeting_room_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> list[Reservation]:
    """Получить информацию по резервом переговорной комнаты."""
    await check_meeting_room_exists(meeting_room_id, session)
    reservations = await reservation_crud.get_future_reservations_for_room(
        room_id=meeting_room_id,
        session=session,
    )
    return reservations
