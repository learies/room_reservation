from fastapi import status

from fastapi.testclient import TestClient


def test_get_all_meeting_rooms(client: TestClient):
    """Тест GET запроса на получение списка переговорок.

    Эндпоинт должен быть доступен для все пользователей.

    Запрос должен отрабатывать как при наличии переговорок в db,
    так и при их отсутствии переговорок в db.

    При отсутствии переговорок в db, должен возвращаться пустой список.
    """
    response = client.get("/api/v1/meeting_rooms/")
    assert (
        response.status_code == status.HTTP_200_OK,
    ), "При GET-запросе к эндпоинту `/api/v1/meeting_rooms/` должен возвращаться статус-код 200."
    assert (
        isinstance(response.json(), list),
    ), "При GET-запросе к эндпоинту `/api/v1/meeting_rooms/` должен возвращаться объект типа `list`."
