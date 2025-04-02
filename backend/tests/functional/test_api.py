import pytest
from faker import Faker

def test_create_and_redirect(client):
    fake = Faker()
    login, password = fake.user_name(), fake.password()
    # Сначала создаем пользователя
    response = client.post(
        "/user/create",
        json={"login": login, "password": password}
    )
    assert response.status_code == 200
    # Авторизуемся
    response = client.post(
        "/user/auth",
        json={"login": login, "password": password}
    )
    assert response.status_code == 200

    access_token = response.json().get('access_token')
    # Сокращаем ссылку
    response = client.post(
        "/links/shorten",
        json={"original_url": "https://example.com"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    short_code = response.json()["short_code"]

    response = client.get(f"/links/{short_code}", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["location"] == "https://example.com"


def test_create_user(client):
    fake = Faker()
    response = client.post(
        "/user/create",
        json={"login": fake.user_name(), "password": fake.password()}
    )
    assert response.status_code == 200


# @pytest.mark.asyncio
# async def test_redis_calls(client, mock_redis):
#     # Настраиваем возвращаемые значения
#     mock_redis.redis.get.return_value = "cached_value"
#
#     response = client.get("/some-cached-endpoint")
#
#     assert response.status_code == 200
#     mock_redis.redis.get.assert_awaited_once_with("cache_key")
#     assert response.json() == {"value": "cached_value"}