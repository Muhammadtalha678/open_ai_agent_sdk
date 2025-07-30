from fastapi import APIRouter,Request
from src.models.Todo_Model import TodoModel
from typing import List

router = APIRouter()



@router.get("/todos")
def get_all_todos(request:Request):
    db = request.app.state.database
    todos = list(db['todos'].find({}))
    todos = [{**todo,'_id':str(todo['_id'])} for todo in todos]
# todo['_id'] = str(todo['_id'])
    # print(todos) 
    return {"message":"Todos fetch successfully",'todos':todos}

@router.post("/addTodo")
def add_todo(request:Request,todo:TodoModel):
    db = request.app.state.database
    todo_dict = todo.model_dump() # use todo.model_dump() if you use pydantic v2
    todos = db['todos'].insert_one(todo_dict)
    print(todo)
    return todo


