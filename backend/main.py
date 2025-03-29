from fastapi import FastAPI, HTTPException, Query
from routers import users, links
import uvicorn

app = FastAPI()

app.include_router(users.router)
app.include_router(links.router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        access_log=True
    )
