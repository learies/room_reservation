from fastapi import APIRouter

from app.api.v1.endpoints import meeting_room_router

main_router = APIRouter(prefix="/api/v1")
main_router.include_router(
    meeting_room_router, prefix="/meeting_rooms", tags=["Meeting Rooms"]
)
