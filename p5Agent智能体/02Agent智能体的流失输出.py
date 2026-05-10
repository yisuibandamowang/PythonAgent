from langchain.agents import create_agent
from langchain_community.chat_models import ChatTongyi
from dotenv import load_dotenv
import os

from langchain_core.tools import tool

load_dotenv()
ali_api_key = os.getenv("ALI_API_KEY")

@tool(description="获取股价，传入股票名称，返回股票信息")
def get_price(name):
    return f"股票{name}的价格是100"

@tool(description="获取股票信息，传入股票名称，返回股票信息")
def get_info(name):
    return f"股票{name}的信息是：股票名称：{name}，股票价格：100,{name}是一家上市公司，专注于AI科技"

agent = create_agent(
    model=ChatTongyi(model="qwen3-max",api_key=ali_api_key),
    tools=[get_price,get_info],
    system_prompt="你是一个帮助用户查询股票信息的助手，你可以使用get_price和get_info两个工具来查询股票信息。并且要告知我思考过程，告诉我你为什么调用某个工具",
)

for chunk in agent.stream(
    {"messages":[{"role":"user","content":"小黑科技股票价格如何？并简单介绍一下这支股票"}]},
    stream_mode="values"
):
    latest_message = chunk["messages"][-1]

    if latest_message.content:
        print(type(latest_message).__name__,latest_message.content)

    try:
        if latest_message.tool_calls:
            print(type(latest_message).__name__,latest_message.tool_call.name,latest_message.tool_call.args)
    except:
        pass

