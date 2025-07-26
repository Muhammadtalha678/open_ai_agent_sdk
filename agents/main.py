from agents import Agent,Runner,RunConfig,AsyncOpenAI,OpenAIChatCompletionsModel,function_tool,SQLiteSession,ModelSettings
from dotenv import load_dotenv
import os
import asyncio
from dataclasses import dataclass
load_dotenv()
from pydantic import BaseModel

Gemini_Api_Key = os.getenv('GEMINI_API_KEY')
Base_Url = os.getenv('GOOGLE_GEMINI_BASE_URL')

client = AsyncOpenAI(
    api_key=Gemini_Api_Key,
    base_url=Base_Url
)

model = OpenAIChatCompletionsModel(
    model='gemini-1.5-flash',
    openai_client=client
)
runConfig = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True,
    # model_settings=ModelSettings(
    #     temperature=0.7,
    # )
)
class UserEvent(BaseModel):
    uid:str
    plan:str
    # description:str
@dataclass
class UserContext:
    uid:str

    async def get_plan(self):
        if self.uid == '1':
            return "Enterprise"
        elif self.uid == '2':
            return "Pro"
        elif self.uid == '3':
            return "Basic"
        else:
            return "User Id not found"


@function_tool
async def show_user_plan(context:UserContext) -> str:
    """
    Use this tool when the user asks about their current subscription plan, features, or privileges.

    This tool checks the user's unique ID and returns their current plan: Basic, Pro, or Enterprise.
    Always call this function when the response needs to be personalized based on the user’s plan.

    Args:
        context: Automatically injected. Includes the user's UID and methods to get user data.

    Returns:
        A string indicating the user's current plan level.
    """
    print("context",context)
    return await context.get_plan()


agent = Agent[UserContext](
    name="Assistant",
    instructions="you are UserInfo fetch Assistant",
    tools=[show_user_plan],
    output_type=UserEvent
    )

async def main():
    session = SQLiteSession(session_id="converstaion_123")
    try:
        while True:
            query = input("Enter the query:")
            if query.lower() == "quit":
                print("Exiting...")
                break 
            result = await Runner.run(
                agent,
                input= query,
                context=UserContext(uid="2"),
                run_config=runConfig,
                session=session,

            )
            print(result.final_output)
    except Exception as e:
        print("error",e)
    
if __name__ == '__main__':
    asyncio.run(main())     


