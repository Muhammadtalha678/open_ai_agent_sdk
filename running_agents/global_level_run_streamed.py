import os
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner,set_tracing_disabled,RunConfig
from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv
import asyncio

load_dotenv()

gemini_api_key = os.getenv('GOOGLE_API_KEY')
# set_tracing_disabled(True)
client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model= OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)
        
config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
)

async def main():
    try:
        agent = Agent(
        name="Assistant",
        instructions="You are an AI expert.",
        )
        query = input("Enter the query:")
        result = Runner.run_streamed(agent, input=query,run_config=config)
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta, end="", flush=True)

    except Exception as e:
        print(e)

asyncio.run(main())   