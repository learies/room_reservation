from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.meeting_room import MeetingRoom
from app.schemas.meeting_room import MeetingRoomCreate, MeetingRoomUpdate


@dataclass
class CRUDMeetingRoom(
    CRUDBase[
        MeetingRoom,
        MeetingRoomCreate,
        MeetingRoomUpdate,
    ]
):
    """CRUD методы для модели переговорок.

    Args:
        model (Type[MeetingRoom]): Модель переговорок.
    """

    async def get_all_active(
        self,
        session: AsyncSession,
    ) -> list[MeetingRoom]:
        """Получить список активных переговорок.

        Args:
            session (AsyncSession): Сессия базы данных.

        Returns:
            list[MeetingRoom]: Список переговорок.
        """
        db_objs = await session.scalars(
            select(self.model).where(
                # Эквивалентно self.model.is_active == True
                self.model.is_active.is_(True),
            )
        )
        return db_objs.all()

    async def get_room_id_by_name(
        self,
        room_name: str,
        session: AsyncSession,
    ) -> int | None:
        """Получить идентификатор id переговорки по названию.

        Args:
            room_name (str): Название переговорки.
            session (AsyncSession): Сессия базы данных.

        Returns:
            int: Идентификатор переговорки.
        """
        db_room_id = await session.scalars(
            select(self.model.id).where(
                self.model.name == room_name,
            )
        )
        return db_room_id.first()

    async def get_room_by_name(
        self,
        room_name: str,
        session: AsyncSession,
    ) -> MeetingRoom | None:
        """Получить переговорку по названию.

        Args:
            room_name (str): Название переговорки.
            session (AsyncSession): Сессия базы данных.

        Returns:
            MeetingRoom | None: Объект переговорки.
        """
        meeting_room = await session.scalars(
            select(self.model).where(
                self.model.name == room_name,
            )
        )
        return meeting_room.first()


meeting_room_crud = CRUDMeetingRoom(MeetingRoom)
