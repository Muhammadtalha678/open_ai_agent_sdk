# def main():
#     print("Hello from basic-cover!")


# if __name__ == "__main__":
#     main()
# Global Configration use by each agent 

from agents import Agent,Runner,AsyncOpenAI,OpenAIChatCompletionsModel,RunConfig,set_tracing_disabled
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('GOOGLE_API_KEY')
BASE_URL = os.getenv('GOOGLE_GEMINI_BASE_URL')
# print(API_KEY)
set_tracing_disabled(True)
client = AsyncOpenAI(
    api_key=API_KEY,base_url=BASE_URL
)


first_agent = Agent(name="Assistant", instructions="You are a helpful assistan",model=OpenAIChatCompletionsModel(
    model="gemini-2.5-pro",openai_client=client,
))

query = input("Ask any question from my Agent") 
result = Runner.run_sync(
    starting_agent=first_agent,
    input=query,
    
)

print(result.final_output)