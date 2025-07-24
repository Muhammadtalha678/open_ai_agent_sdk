from agents import Agent,Runner,RunConfig,AsyncOpenAI,OpenAIChatCompletionsModel
from dotenv import load_dotenv
import os
import asyncio
load_dotenv()
API_KEY = os.getenv('GOOGLE_API_KEY')

BASE_URL = os.getenv('GOOGLE_GEMINI_BASE_URL')

client = AsyncOpenAI(
    api_key=API_KEY,base_url=BASE_URL
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-pro",openai_client=client
)

runConfig = RunConfig(
    model=model,tracing_disabled=True
)

agent = Agent(
 name="Assistant",instructions="You are my Assistant Agent"
)

async def main():
     result = await Runner.run(
          starting_agent=agent,input="Capital of france",run_config=runConfig
     ) 
     print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main()) 