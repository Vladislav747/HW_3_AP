from fastapi import FastAPI, HTTPException, Query
from routers import users, links
import uvicorn

from redis_utils import redis_cache

app = FastAPI()

app.include_router(users.router)
app.include_router(links.router)

@app.on_event("startup")
async def startup():
    await redis_cache.init_redis()

@app.on_event("shutdown")
async def shutdown():
    await redis_cache.close()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        access_log=True
    )
