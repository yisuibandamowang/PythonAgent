from langchain.agents import create_agent
from langchain_community.chat_models import ChatTongyi
from dotenv import load_dotenv
import os
from langchain_core.tools import tool

load_dotenv()
api_key = os.getenv("ALI_API_KEY")
model = ChatTongyi(model="qwen3-max",api_key=api_key)

@tool(description="获取天气")
def get_weather() -> str:
    return "今天天气晴朗，适合出门"

agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt="你是一个有用的助手，可以回答任何问题。",
)


res = agent.invoke(
    {
        "messages":[
            {"role":"user","content":"你好，请问今天的天气如何？"},
        ]
    }
)

for message in res["messages"]:
    print(type(message).__name__,message.content)