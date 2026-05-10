from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import before_agent, after_agent, before_model, after_model, wrap_model_call, \
    wrap_tool_call
from langchain_community.chat_models import ChatTongyi
from dotenv import load_dotenv
import os
from langchain_core.tools import tool
from langgraph.runtime import Runtime

load_dotenv()
api_key = os.getenv("ALI_API_KEY")
model = ChatTongyi(model="qwen3-max",api_key=api_key)

@tool(description="获取天气")
def get_weather() -> str:
    return "今天天气晴朗，适合出门"

"""
六个可拦截节点：
1.agent执行前
2.agent执行后
3.model执行前
4.model执行后
5.工具执行中
6.模型执行中
"""

@before_agent
def before_agent_middleware(state:AgentState,runtime:Runtime) -> None:
    print("agent执行前")

@after_agent
def log_after_agent_middleware(state:AgentState,runtime:Runtime) -> None:
    print("agent执行后")

@before_model
def before_model_middleware(state:AgentState,runtime:Runtime) -> None:
    print("model执行前")

@after_model
def log_after_model_middleware(state:AgentState,runtime:Runtime) -> None:
    print("model执行后")

@wrap_model_call
def model_call_hook(request,handler):
    print("模型执行中")
    return handler(request)

@wrap_tool_call
def tool_call_hook(request,handler):
    print("工具执行中")
    print(f"工具执行：{request.tool_call['name']}")
    print(f"工具执行参数：{request.tool_call['args']}")
    return handler(request)

agent = create_agent(
    model=model,
    tools=[get_weather],
    middleware=[
        before_agent_middleware,
        log_after_agent_middleware,
        before_model_middleware,
        log_after_model_middleware,
        model_call_hook,
        tool_call_hook
    ],
    system_prompt="你是一个有用的助手，可以回答任何问题。",
)

res = agent.invoke({"messages":[{"role":"user","content":"大连今天的天气如何，我该如何穿衣？"}]})
print("*"*20,res)