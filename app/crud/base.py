from dataclasses import dataclass
from typing import Generic, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


@dataclass
class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    model: Type[ModelType]

    async def get_all(
        self,
        session: AsyncSession,
    ) -> list[ModelType]:
        """Получить список объектов.

        Args:
            session (AsyncSession): Сессия базы данных.

        Returns:
            list[ModelType]: Список объектов.
        """
        db_objs = await session.scalars(select(self.model))
        return list(db_objs.all())

    async def get_by_id(
        self,
        obj_id: int,
        session: AsyncSession,
    ) -> ModelType | None:
        """Получить объект по идентификатору id.

        Args:
            obj_id (int): Идентификатор объекта.
            session (AsyncSession): Сессия базы данных.

        Returns:
            ModelType: Полученный объект.
        """
        return await session.get(self.model, obj_id)

    async def create(
        self,
        obj_in: CreateSchemaType,
        session: AsyncSession,
    ) -> ModelType:
        """Создать объект.

        Args:
            obj_in (CreateSchemaType): Входные данные для нового объекта.
            session (AsyncSession): Сессия базы данных.

        Returns:
            ModelType: Созданный объект.
        """
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db_obj: ModelType,
        obj_in: UpdateSchemaType,
        session: AsyncSession,
    ) -> ModelType:
        """Обновить объект.

        Args:
            db_obj (ModelType): Объект для обновления.
            obj_in (UpdateSchemaType): Входные данные для обновления.
            session (AsyncSession): Сессия базы данных.

        Returns:
            ModelType: Обновленный объект.
        """
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj: ModelType,
        session: AsyncSession,
    ) -> ModelType:
        """Мягкое удаление объекта.

        Args:
            db_obj (ModelType): Объект для удаления.
            session (AsyncSession): Сессия базы данных.

        Returns:
            ModelType: Удаленный объект.
        """
        db_obj.is_active = False
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def restore(
        self,
        db_obj: ModelType,
        obj_in: UpdateSchemaType,
        session: AsyncSession,
    ) -> ModelType:
        """Восстановить удалённый объект.

        Args:
            db_obj (ModelType): Объект для восстановления.
            obj_in (UpdateSchemaType): Входные данные для обновления.
            session (AsyncSession): Сессия базы данных.

        Returns:
            ModelType: Восстановленный объект.
        """
        obj_data = jsonable_encoder(db_obj)
        restore_data = obj_in.model_dump(exclude_unset=True)

        for field, value in restore_data.items():
            setattr(db_obj, field, value)

        db_obj.is_active = True
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
