Сервис для укорачивания ссылок


# Описание логики и роутов

Сервис содержит postgres, redis и развернут в докере

## Описание логики

1. **Регистрация пользователя**:
    - `POST /user/create` - создание нового пользователя

2. **Авторизация**:
    - `POST /user/auth` - получение Bearer токена (действует 5 минут)
    - Токен передается в заголовке: `Authorization: Bearer <token>`

3. **Работа с ссылками**:
    - Создание, удаление и изменение ссылок требуют авторизации - нужно вставлять использовать в  BEARER access_token который получили при авторизации
    - Используется кэширование Redis для ускорения работы
    - Выводится список истекших ссылок по роуту GET links/expired
    - Инвалидация кэша при удалении и изменении


## Роуты для работы с ссылками (`/links`)

### 1. Создание короткой ссылки

**Endpoint**: `POST /links/shorten`

**Параметры**:
```json
{
  "original_url": "string (URL)",
  "custom_alias": "string (опционально)"
}
```


2. Поиск ссылки по оригинальному URL
   Endpoint: GET /links/search?original_url=<URL>

Кэширование: 5 минут (prefix="links")

3. Удаление ссылки
   Endpoint: DELETE /links/{short_code}

4. Обновление ссылки
   Endpoint: PUT /links/{short_code}

**Параметры**:
```json
{
  "new_url": "string (новый URL)"
}
```

5. Получение истекших ссылок
   Endpoint: GET /links/expired


6. Получение статистики по ссылке
   Endpoint: GET /links/{short_code}/stats


7. Редирект по короткой ссылке
   Endpoint: GET /links/{short_code}

    Логика:
    
    Перенаправляет на оригинальный URL (302 Redirect)


## Роуты для работы с пользоваетелем (`/user`)

### 1. Создание нового пользователя

**Endpoint**: `POST /user/create`

**Параметры**:
```json
{
  "login": "string (уникальный логин)",
  "password": "string (пароль)"
}
```

2. Аутентификация пользователя
   Endpoint: POST /user/auth


**Параметры**:
```json
{
  "login": "string (уникальный логин)",
  "password": "string (пароль)"
}
```


3. Получение информации о пользователе
   Endpoint: GET /user/user_info/{username}

   Логика:
   
   Находит пользователя по логину
   
   Возвращает основные данные

# Дополнительная инфомация для локальной разработки

#### Настройка локально окружения

```
python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

# запуск локально в папке backend
uvicorn main:app --reload
```

Открывается дефолтно на этом порту

```
http://localhost:8000
```

#### Документация Swagger
```
http://localhost:8000/docs
```

#### При начале работы с postgres

Выполнить инициализацию БД в папке backend

```
python init_db.py
```

Применить миграции в папке backend

```
alembic upgrade head
```

Откатить все миграции(если нужно)
```
alembic downgrade base 
```