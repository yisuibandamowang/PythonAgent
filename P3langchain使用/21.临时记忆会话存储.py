from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser,StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("ALI_API_KEY")
model = ChatTongyi(model="qwen3-max",api_key=api_key)

prompt = PromptTemplate.from_template(
    "你需要根据会话历史回应用户问题。对话历史：{chat_history},用户问题：{user_question}，请根据会话历史回答用户问题"
)

str_parser = StrOutputParser()
json_parser = JsonOutputParser()

def print_prompt(inputs):
    print("=" * 20 ,inputs.to_string() ,"=" * 20)
    return inputs

base_chain = prompt | print_prompt | model | str_parser

store = {} #key session,value 就是 inmemorychatmessagehistory 类对象

def getHistory(session_id):
    if(session_id not in store):
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# 创建一个新的 chain 增强原始 chain
conversation_chain = RunnableWithMessageHistory(
    base_chain, #被增强的原有链
    getHistory, # 通过会话id获取历史数据
    input_messages_key="user_question", #用户输入在模版中的占位符
    history_messages_key="chat_history", #历史数据在模版中的占位符
)

if __name__ == "__main__":
    session_config = {
        "configurable":{
            "session_id": "user_001"
        }
    }
    res = conversation_chain.invoke(input={"user_question": "小明有1只狗"}, config=session_config)
    print(res)

    res = conversation_chain.invoke(input={"user_question": "小刚有4只猫"}, config=session_config)
    print(res)

    res = conversation_chain.invoke(input={"user_question": "总共有几只宠物？"}, config=session_config)
    print(res)



