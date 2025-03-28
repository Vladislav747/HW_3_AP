Сервис для укорачивания ссылок

- swagger доступен по ссылке

```
python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

# локально в папке backend
uvicorn app.main:app --reload
```

Открывается тут

```
http://localhost/
```

инициализация БД

```
python init_db.py
```