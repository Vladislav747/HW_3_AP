import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    # Создаем mock для RedisCache
    mock_redis = MagicMock()
    mock_redis.redis = AsyncMock()
    mock_redis.init_redis = AsyncMock()
    mock_redis.close = AsyncMock()

    # Подменяем redis_cache
    with patch('main.redis_cache', mock_redis):
        with TestClient(app) as client:
            yield client