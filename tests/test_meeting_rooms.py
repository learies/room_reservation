from fastapi import status

from fastapi.testclient import TestClient


def test_get_all_meeting_rooms(client: TestClient):
    response = client.get("/api/v1/meeting_rooms/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json(), list
