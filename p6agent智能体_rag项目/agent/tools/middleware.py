from typing import Callable

from langchain.agents import AgentState
from langchain.agents.middleware import wrap_tool_call, before_model, dynamic_prompt, ModelRequest
from langchain_core.messages import ToolMessage
from langgraph.prebuilt.tool_node import ToolCallRequest
from langgraph.runtime import Runtime
from langgraph.types import Command
from p6agent智能体_rag项目.utils.logger_handler import logger
from p6agent智能体_rag项目.utils.prompts_loader import load_report_prompts,load_system_prompts

@wrap_tool_call
def monitor_tool(
        request:ToolCallRequest,     # 请求数据封装
        handler:Callable[[ToolCallRequest],ToolMessage | Command]      # 执行的函数本身
) -> ToolMessage | Command:      # 监控工具调用
    logger.info(f"[monitor_tool]执行工具： {request.tool_call['name']}")
    logger.info(f"[monitor_tool]传入参数： {request.tool_call['args']}")
    try:
        result = handler(request)
        logger.info(f"[tool monitor]工具{request.tool_call['name']}执行完成，返回结果：{result}")

        if request.tool_call["name"] == "fill_context_for_report":
            request.runtime.context["report"] = True
        return result
    except Exception as e:
        logger.error(f"[tool monitor]工具{request.tool_call['name']}执行失败，错误信息：{e}")
        raise e

@before_model
def log_before_model(
        state: AgentState,       # 整个agent中的执行状态记录
        runtime: Runtime,        # 运行时上下文信息
):         # 记录模型执行前的信息
    logger.info(f"[log_before_model]即将调用模型，带有{len(state['messages'])}条消息。")
    if state['messages']:
        logger.debug(f"[log_before_model]{type(state['messages'][-1]).__name__} | {state['messages'][-1].content.strip()}")

    return None

@dynamic_prompt     # 每一次在生成提示词之前调用
def report_prompt_switch(request: ModelRequest):       # 报告提示词切换
    is_report = request.runtime.context.get("report", False)
    print("*"*30)
    if is_report:
        logger.info(f"[report_prompt_switch]报告提示词切换为：{load_report_prompts()}")
        return load_report_prompts()
    return load_system_prompts()
