# Тестирование 

```
cd tests/unit

pytest -s -v
```

Запуск coverage

```
coverage run -m pytest tests/
```

```
pytest -s -v tests/functional
```

Запуск нагрузочного тестирования
```
locust -f tests/load_testing/locustfile.py
```