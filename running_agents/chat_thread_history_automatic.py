from agents import Agent,RunConfig,Runner,OpenAIChatCompletionsModel,set_tracing_disabled,SQLiteSession
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
API_KEY = os.getenv('GOOGLE_API_KEY')

BASE_URL = os.getenv('GOOGLE_GEMINI_BASE_URL')
set_tracing_disabled(True)

client = AsyncOpenAI(
    api_key=API_KEY,base_url=BASE_URL
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-pro",openai_client=client
)

agent = Agent(name="Assistant",instructions="You are a helpful assistant agent",model=model)

async def main():
    print("Type your question. Type 'quit' to exit.\n")
    session = SQLiteSession("conversation_123")
    while True:
        query = input("Enter the query:")
        if query.lower() == "quit":
            print("Exiting...")
            break
        result = await Runner.run(
            agent,query,session=session
        )    
        print(result.final_output)
        # print("session",session.get_items)
if __name__ == "__main__":
    asyncio.run(main())
