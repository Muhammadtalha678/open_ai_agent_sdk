from agents import Agent,Runner,RunConfig,AsyncOpenAI,OpenAIChatCompletionsModel
from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv
import chainlit as cl
# load_dotenv()

client = AsyncOpenAI(
    api_key="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",base_url="https://openrouter.ai/api/v1"
)

model = OpenAIChatCompletionsModel(
    model="openai/gpt-4o-mini",openai_client=client
)

starting_agent = Agent(
    name="Assistant",instructions="you are a helpful agent, Help user with their quries"

)
config = RunConfig(
    model=model,model_provider=client,tracing_disabled=True
)

@cl.on_chat_start
async def chat_start():
    await cl.Message(content="Welcome to chatbot").send()


@cl.on_message
async def on_message(message:cl.Message):
    msg = cl.Message(content="")
    result = Runner.run_streamed(
        starting_agent=starting_agent,input=message.content,run_config=config
    )
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data,ResponseTextDeltaEvent):
            # print(event.data.delta,end="",flush=True)
            await msg.stream_token(event.data.delta) 
    await msg.update()

async def main():
    print("Hello from chainlit-streaming!")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
