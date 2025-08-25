from agents import Agent,Runner,RunConfig,FunctionTool,function_tool,enable_verbose_stdout_logging,ModelSettings,RunContextWrapper,handoff
from dataclasses import dataclass
from pymongo.database import Database
# import src.models.Todo_Model as TodoModel
from src.models.Todo_Model import TodoModel

# TodoModel.TodoModel

# class GetTodoListParams(BaseModel):
#     model_config:ConfigDict(extra="forbid")
    

@dataclass
class DbContext:
    db: Database

    def get_table_todos(self):
        table = self.db['todos']
        return table


def fetch_todos_from_db(db:Database):
    db_table = db['todos']
    todos = list(db_table.find({}))
    todos = [{**todo,'_id':str(todo['_id'])} for todo in todos] 
     print(todos)
    return {"message":"Todos fetch successfully",'todos':todos}


async def run_function(ctx:RunContextWrapper[DbContext],input:str):
    db = ctx.context.db
    print("This is a run function",db)
    # return input
    return fetch_todos_from_db(db=db)


all_todo_tool = FunctionTool(
    name="Todos_Fetcher",
    description=
    """
    Goal:
        Fetch all Todos from MongoDb database.

    Returns:
        All todos
    """,
    params_json_schema={
      "additionalProperties": False,
        "type": "object",
        "properties": {},
        "required": []   
    },
    on_invoke_tool=run_function,
)
@function_tool()
def add_todo_tool(context:RunContextWrapper[DbContext],todos:list[TodoModel]):
    """
    Goal:
        Create multiple todos in MongoDb database.

     Args:
        todos: List of TodoModel with title, description, and optional status.         
    Returns:
        The newly created todo items
    """

    db_table = context.context.get_table_todos()
    inserted = []
    for todo in todos:
        new_todo = todo.model_dump() # use todo.model_dump() if you use pydantic v2
        print(new_todo)
        db_table.insert_one(new_todo)
        inserted.append(new_todo)
    # print(todo)
    return inserted



async def handle_todo_operation(db,agent_config,query):
    mongoDbContext = DbContext(db=db)
    # print(agent_config)
    # enable_verbose_stdout_logging()
    # # return {query}
    runConfig = RunConfig(
        model=agent_config.model(),
        model_provider= agent_config.client(),
        # tracing_disabled=True,
    )

    all_todos_agent = Agent[DbContext](
        name="Fetch All Todos",
        instructions="Fetch all todos from the given tool",
        tools=[all_todo_tool],
        model_settings=ModelSettings(tool_choice="required"),
        handoff_description= "Only fetch the todos if they requested for fetch all todos"
    )
    add_todo_agent = Agent[DbContext](
        name="Add Todo",
         instructions=(
        "Add one or more todos using the given tool. "
        "If the user gives multiple todos in a single query, "
        "combine them into a list and call the tool only once."
        ),
        tools=[add_todo_tool],
        # model_settings=ModelSettings(tool_choice="required")
    )
    starting_agent = Agent(
        name="Todo Agent",
        instructions=(
           "Help the user with their todo requests. "
        "If they ask to see all todos, handoff to the 'Fetch All Todos' agent. "
        "If they ask to add todos, handoff once to the 'Add Todo' agent. "
        "Do not make more than one handoff per query."
        ),
        handoffs=[all_todos_agent,add_todo_agent],
        # tools=[all_todo_tool]
        
        
    )

    result = await Runner.run(
        starting_agent=starting_agent,input = query,run_config=runConfig,context=mongoDbContext
    )
    return result.final_output
    # return "Hello"
