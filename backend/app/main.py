from fastapi import FastAPI, HTTPException, Query
from routes import router

app = FastAPI()

app.include_router(router)
