from fastapi import APIRouter

from app.meeting_room.api.v1 import meeting_room_router

main_router = APIRouter(prefix="/api/v1")
main_router.include_router(
    meeting_room_router, prefix="/meeting_rooms", tags=["Meeting Rooms"]
)
