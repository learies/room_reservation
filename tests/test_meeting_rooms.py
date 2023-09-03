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
    assert response.status_code == status.HTTP_200_OK,\
        "При GET-запросе к эндпоинту `/api/v1/meeting_rooms/` должен возвращаться статус-код 200."
    assert isinstance(response.json(), list),\
        "При GET-запросе к эндпоинту `/api/v1/meeting_rooms/` должен возвращаться объект типа `list`."


def test_create_meeting_rooms(client: TestClient):
    """Тест POST запроса на создание переговорок.

    Эндпоинт должен создать переговорку со статусом 201 и вернуть словарь.
    """
    response = client.post(
        "/api/v1/meeting_rooms/",
        json={
            "name": "Главная переговорка",
            "description": "Очень большая, модная и помпезная комната.",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert isinstance(response.json(), dict)


def test_create_meeting_rooms_which_duplicate_name(client: TestClient):
    """Тест POST запроса на создание переговорок с существующим именем.

    Эндпоинт должен вернуть ошибку 422, поле name должно быть уникальным.
    """
    response = client.post(
        "/api/v1/meeting_rooms/",
        json={
            "name": "Главная переговорка",
            "description": "Очень большая, модная и помпезная комната.",
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY,\
        "При POST-запросе к эндпоинту `/api/v1/meeting_rooms/`, поле name должно быть уникальным."


def test_create_meeting_rooms_which_max_length_name(client: TestClient):
    """Тест POST запроса на создание переговорок с максимальной длинной имени.

    Эндпоинт должен вернуть ошибку 422, если поле name > 100 символов.
    """
    response = client.post(
        "/api/v1/meeting_rooms/",
        json={
            "name": "Г" * 101,
            "description": "Очень большая, модная и помпезная комната.",
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY,\
        "При POST-запросе к эндпоинту `/api/v1/meeting_rooms/`, поле name не должно быть > 100 символов."
