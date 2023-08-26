import pytest

from fastapi.testclient import TestClient

try:
    from app.main import app
except (NameError, ImportError):
    raise AssertionError(
        "Не обнаружен объект приложения `app`."
        "Проверьте и поправьте: он должен быть доступен в модуле `app.main`.",
    )


@pytest.fixture
async def client():
    with TestClient(app) as client:
        yield client
