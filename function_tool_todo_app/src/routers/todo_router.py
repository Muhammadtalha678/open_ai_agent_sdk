from fastapi import APIRouter,Request
from src.models.Todo_Model import TodoModel
from src.models.QueryModel import QueryModel
from typing import List
from src.controllers.todo_controller import handle_todo_operation,fetch_todos_from_db
router = APIRouter()



@router.get("/todos")
def get_all_todos(request:Request):
   db = request.app.state.database
   return fetch_todos_from_db(db)

# @router.post("/addTodo")
# def add_todo(request:Request,todo:TodoModel):
#     db = request.app.state.database
#     return add_todo_tool(db,todo)


@router.post("/query")
async def todo_query(request_query:QueryModel,request:Request):
    db = request.app.state.database
    agent_config = request.app.state.agent_config
    return await handle_todo_operation(agent_config=agent_config,db=db,query=request_query.query)


