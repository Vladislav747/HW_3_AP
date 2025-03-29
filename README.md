Сервис для укорачивания ссылок

- swagger доступен по ссылке

```
python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

# запуск локально в папке backend
uvicorn main:app --reload
```

Открывается тут

```
http://localhost/
```

При начале работы с БД

Выполнить инициализацию БД в папке backend

```
python init_db.py
```

Применить миграции в папке backend

```
alembic upgrade head
```

Откатить все миграции
```
alembic downgrade base 
```