import pytest
from faker import Faker


@pytest.mark.asyncio
async def test_create_and_redirect(async_client):
    fake = Faker()
    login, password = fake.user_name(), fake.password()

    # Создаем пользователя
    response = await async_client.post(
        "/user/create",
        json={"login": login, "password": password}
    )
    assert response.status_code == 200

    # Авторизуемся
    response = await async_client.post(
        "/user/auth",
        json={"login": login, "password": password}
    )
    assert response.status_code == 200

    access_token = response.json().get('access_token')

    # Сокращаем ссылку
    response = await async_client.post(
        "/links/shorten",
        json={"original_url": "https://example.com"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    short_code = response.json()["short_code"]

    # Проверяем редирект
    response = await async_client.get(
        f"/links/{short_code}",
        follow_redirects=False
    )
    assert response.status_code == 302
    assert response.headers["location"] == "https://example.com"


@pytest.mark.asyncio
async def test_create_user(async_client):
    fake = Faker()
    response = await async_client.post(
        "/user/create",
        json={"login": fake.user_name(), "password": fake.password()}
    )
    assert response.status_code == 200


async def test_create_with_alias(client, mock_redis):
    fake = Faker()
    short_code = fake.user_name()

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
        json={"original_url": "https://example.com", "custom_alias": short_code},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    short_code_res = response.json()["short_code"]

    assert short_code_res == short_code


def test_delete_link(client, mock_redis):
    fake = Faker()
    short_code = fake.user_name()

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
        json={"original_url": "https://example.com", "custom_alias": short_code},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    short_code_res = response.json()["short_code"]

    assert short_code_res == short_code

    response = client.delete(
        f"/links/{short_code}",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200


def test_stats_link(client, mock_redis):
    fake = Faker()
    short_code = fake.user_name()

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
        json={"original_url": "https://example.com", "custom_alias": short_code},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    short_code_res = response.json()["short_code"]

    assert short_code_res == short_code

    response = client.get(
        f"/links/{short_code}/stats",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200

async def test_search_param_link(async_client, mock_redis):
    fake = Faker()

    short_code = 'asdasd'
    original_url = "https://yandex.com"

    login, password = fake.user_name(), fake.password()
    # Сначала создаем пользователя
    response = await async_client.post(
        "/user/create",
        json={"login": login, "password": password}
    )
    assert response.status_code == 200
    # Авторизуемся
    response = await async_client.post(
        "/user/auth",
        json={"login": login, "password": password}
    )
    assert response.status_code == 200

    access_token = response.json().get('access_token')

    response = await async_client.delete(
        f"/links/{short_code}",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    response = await async_client.post(
        "/links/shorten",
        json={"original_url": original_url, "custom_alias": short_code},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    short_code_res = response.json()["short_code"]

    assert short_code_res == short_code

    response_search = await async_client.get(
        f"/links/search?original_url={original_url}",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200

    short_code_res = response_search.json()["short_code"]

    assert short_code_res == short_code


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