from agents import Agent,Runner,RunConfig,AsyncOpenAI,OpenAIChatCompletionsModel,function_tool,SQLiteSession,ModelSettings,RunContextWrapper
from dotenv import load_dotenv
import asyncio
import os
import re
from dataclasses import dataclass
from pydantic import BaseModel
from typing import List
import uuid
load_dotenv()

Gemini_Api_Key = os.getenv('GEMINI_API_KEY')
Base_Url = os.getenv('GOOGLE_GEMINI_BASE_URL')

client = AsyncOpenAI(
    api_key=Gemini_Api_Key,
    base_url=Base_Url
)

model = OpenAIChatCompletionsModel(
    model='openai/gpt-4o-mini',
    # model='google/gemini-flash-1.5',
    openai_client=client
)

class UserEvent(BaseModel):
    # uid:str
    plan:str
#     # description:str
@dataclass
class UserContext:
    uid:List[str]
    

    async def get_plan(self)->str:
        plans=[]
        for user_id in self.uid:    
            if user_id == '1':
                
                plans.append(f"User {user_id}: Enterprise")
            elif user_id == '2':
                
                plans.append(f"User {user_id}: Pro")           
            elif user_id == '3':
                
                plans.append(f"User {user_id}: Basic")           
            else:
                
                plans.append(f"User {user_id}: Not Found")           
        return ", ".join(plans) # User 1: Enterprise, User 2: Pro, User 3: Basic


@function_tool()
async def show_user_plan(context:RunContextWrapper[UserContext]) -> str:
    print("Tool Execution ID:", uuid.uuid4())

    """
    Use this tool ONLY if the query asks about a user's plan AND the user ID is present.
    Supports multiple user IDs.

    Args:
        context: Automatically injected. Includes the user's UID and methods to get user data.

    """
    print("context",context)
    return await context.context.get_plan()

user_info_agent = Agent[UserContext](
    name="User Info Assistant",
    instructions="you are the User Info Assistant",
    tools=[show_user_plan],
    model_settings=ModelSettings(
    #     tool_choice="required"
        tool_choice="required"
    ),
    output_type=UserEvent,
)

agent = Agent(
    name="Assistant",
    instructions=(
        "You are a helpful assistant. Help the user with their Questions"
        "Only handsoffs to the user_info_agent when user provide the id of plan"
        ),
    handoffs=[user_info_agent],
    handoff_description="Use this agent when the user asks about their subscription plan and provides a id."
    )
runConfig = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True,
    model_settings=ModelSettings(
        temperature=0.7,
    )
)
# def extract_uid(query: str) -> str:
#     print(query)
#     match = re.search(r'user\s*(\d+)', query.lower())
#     if match:
#         return match.group(1)
#     return "unknown"
def extract_uids(query: str) -> list[str]:
    # Find all digit patterns in the input
    return re.findall(r'\b\d+\b', query) # ['1', '2', '3']

async def main():
    session = SQLiteSession(session_id="converstaion_123")
    try:
        while True:
            query = input("Enter the query:")
            if query.lower() == "quit":
                print("Exiting...")
                break 
            uid = extract_uids(query)
            # print(uid) 
            result = await Runner.run(
                agent,
                input= query,
                context=UserContext(uid=uid),
                run_config=runConfig, 
                session=session,
                
            )
            print(result.final_output)
    except Exception as e:
        print("error",e)
    
if __name__ == '__main__':
    asyncio.run(main())     
