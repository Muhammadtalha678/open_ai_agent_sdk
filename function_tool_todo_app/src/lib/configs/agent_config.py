from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,RunConfig,Runner
from dataclasses import dataclass

@dataclass
class AgentConfig:
    base_url:str
    api_key:str
    model_name:str

    def client(self):
        return AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
    def model(self):
        return OpenAIChatCompletionsModel(
            model=self.model_name,
            openai_client=self.client()
        )
    
    
