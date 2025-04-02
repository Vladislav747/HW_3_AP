import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from main import app
from redis_utils import RedisCache

@pytest.fixture
def mock_redis(mocker):
    mock = mocker.MagicMock(spec=RedisCache)
    mock.redis = mocker.AsyncMock()
    mock.init_redis = mocker.AsyncMock()
    mock.close = mocker.AsyncMock()
    return mock

@pytest.fixture
async def async_client(mock_redis, mocker):
    # Подменяем redis_cache на mock_redis для тестирования
    mocker.patch('main.redis_cache', mock_redis)
    async with AsyncClient(base_url="http://localhost:8000") as client:
        yield client

# Отдельно синхронный клиент
@pytest.fixture
async def client(mock_redis, mocker):
    # Подменяем redis_cache на mock_redis для тестирования
    mocker.patch('main.redis_cache', mock_redis)
    with TestClient(app) as client:
        yield client


def test_user_creation(client, mock_redis):
    mock_redis.redis.set.return_value = True

    response = client.post(
        "/user/create",
        json={"login": "testuser", "password": "testpass"}
    )

    assert response.status_code == 200
    mock_redis.redis.set.assert_called_once()