from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.lib.db.connect_db import ConnectDb
from contextlib import asynccontextmanager
import uvicorn
from fastapi import Request
from src.routers.todo_router import router as TodoRouter
from src.lib.configs.agent_config import AgentConfig
import src.lib.configs.env_config as env_config 

@asynccontextmanager
async def lifespan(app:FastAPI):
    db = ConnectDb(env_config.mongo_uri)
    await db.connection()
    print("Db connection Started!")
    config_agent = AgentConfig(
        base_url=env_config.base_url,
        api_key=env_config.api_key,
        model_name=env_config.model_name
    )
    app.state.database = await db.get_database()
    app.state.agent_config = config_agent 
    yield
    await db.close_connection()
    print("Db connection closeed!")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
     allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers

)

@app.get('/')
async def root(request:Request):
    return {"message":"Hello world!"} 

app.include_router(TodoRouter,prefix='/api')

if __name__ == "__main__":
    uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True)