from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate


class UserRead(BaseUser[int]):
    ...


class UserCreate(BaseUserCreate):
    ...


class UserUpdate(BaseUserUpdate):
    ...
