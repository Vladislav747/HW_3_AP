from database import engine, Base

# Создаем таблицы в базе данных
# Создает таблицу links, если ее нет.
Base.metadata.create_all(bind=engine)
