import asyncio
from agents import Agent, RunConfig,Runner,OpenAIChatCompletionsModel,set_default_openai_client,set_tracing_export_api_key
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
import chainlit as cl
# from chainlit.utils import mount_chainlit
from fastapi import FastAPI
load_dotenv()

base_url=os.getenv("OPENROUTER_BASE_URL")
api_key=os.getenv("OPENROUTER_API_KEY")



history = []
MAX_HISTORY = 10


models = {
      "Openai":"openai/gpt-4o-mini",
      "DeepSeek":"deepseek/deepseek-r1-0528:free",
      "Gemini-2.0-Flash":"google/gemini-2.0-flash-exp:free",
}
# model_name:str = models["DeepSeek"]
@cl.on_chat_start
async def chat_start():
    await cl.Message(content="Hello from Multiple llm system").send()
    settings = await cl.ChatSettings(
          inputs=[
                cl.input_widget.Select(
                      id  =  "Model",
                      label = "Choose any LLM Model",
                      initial_index  =  0,
                      values = list(models.keys()),
                )
          ]
    ).send()
    await seting_update(settings)

@cl.on_settings_update
async def seting_update(setting):
    cl.user_session.set('model',models[setting['Model']])
    # print('model..',cl.user_session.get('model'))
    await cl.Message(content=f"You have change model to {setting['Model']}").send()

@cl.on_message
async def on_message(message:cl.Message):
        history.append({"role":"user","content":message.content}) 
        modelName = cl.user_session.get('model')
        trimmed_history = history[-MAX_HISTORY:]

        client = AsyncOpenAI(
            base_url=base_url,api_key=api_key
        )

        model = OpenAIChatCompletionsModel(
            model=modelName,
            openai_client=client
        )
        config = RunConfig(
            model=model,model_provider=client,tracing_disabled=True
        )
        chainlit_agent = Agent(name="Assistant",instructions="You are a helpful Assistant")

        
        result = await Runner.run(
        starting_agent=chainlit_agent,input=trimmed_history,
        run_config=config
        )
        await cl.Message(content=result.final_output).send()
        print(result.final_output)
        # print("model_name",modelName)
