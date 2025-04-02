import pytest
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
def client(mock_redis, mocker):
    mocker.patch('main.redis_cache', mock_redis)
    with TestClient(app) as client:
        yield client

# tests/test_users.py
def test_user_creation(client, mock_redis):
    # Настраиваем mock
    mock_redis.redis.set.return_value = True

    response = client.post(
        "/user/create",
        json={"login": "testuser", "password": "testpass"}
    )

    assert response.status_code == 200
    mock_redis.redis.set.assert_called_once()