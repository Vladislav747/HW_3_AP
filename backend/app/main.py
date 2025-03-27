from fastapi import FastAPI, HTTPException, Query
from routes import router

app = FastAPI()

# Подключаем роутер
app.include_router(router)
