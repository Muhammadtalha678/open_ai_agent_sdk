from fastapi import FastAPI
from src.lib.db.connect_db import ConnectDb
from contextlib import asynccontextmanager
from src.lib.configs.env_config import mongo_uri
import uvicorn
from fastapi import Request
from src.routers.todo_router import router as TodoRouter

@asynccontextmanager
async def lifespan(app:FastAPI):
    db = ConnectDb(mongo_uri)
    await db.connection()
    print("Db connection Started!")
    app.state.database = await db.get_database()
    yield
    await db.close_connection()
    print("Db connection closeed!")

app = FastAPI(lifespan=lifespan)

@app.get('/')
async def root(request:Request):
    return {"message":"Hello world!"} 

app.include_router(TodoRouter,prefix='/api')

if __name__ == "__main__":
    uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True)